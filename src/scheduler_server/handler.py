from datetime import datetime
import os
import importlib
import yaml
import os, os.path as op
import random
import logging

logger = logging.getLogger(__name__)

from .utils import split_into_parts, send_request

random.seed(int(datetime.now().timestamp()))


def dummy_handler(t0, t1, policy_config={}):
    dt = abs(t1.timestamp() - t0.timestamp())  # too lazy to check for t1<t0 now
    # get current time as a timestamp string
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    n = random.randint(1, 10)
    parts = split_into_parts(dt, n)
    commands = ["import time", f"# {now}"]
    for i, part in enumerate(parts):
        commands += [f"time.sleep({part:.2f})"]
    commands = "\n".join(commands)
    return commands


def rest_handler(t0, t1, policy_config={}):
    url = policy_config.pop('url')
    headers = policy_config.pop('headers', {})
    queries = policy_config.pop('queries', {})
    response = send_request(url, headers, queries)

    plans = response['list']

    # identify active plans
    plans = [p for p in plans if p['status'] == 'active']
    if len(plans) == 0:
        raise ValueError("No active plans found")

    # is there a plan that covers the full interval?
    request_tot_sec = (t1-t0).total_seconds()

    plans_overlap = []
    for plan in plans:
        t_beg = datetime.fromisoformat(plan['from'])
        t_end = datetime.fromisoformat(plan['to'])

        plan_tot_sec = (t_end - t_beg).total_seconds()
        overlap_sec = max((min(t1, t_end) - max(t0, t_beg)).total_seconds(), 0)
        overlap_frac = overlap_sec / request_tot_sec
        if overlap_frac > 0:
            plans_overlap.append((overlap_frac, t_beg, plan))

    if len(plans_overlap) == 0:
        raise ValueError("No active plan has any overlap with the requested period")

    # sort to find plan with maximal overlap
    best_plan = sorted(plans_overlap, key=lambda x: (-x[0], x[1]))[0][-1]  # largest overlap and earliest in time.
    logger.info(f"Best plan found: {best_plan}")
    program = best_plan['program']

    # expect active_plan['config'] to be a yaml expr, but it will
    # also load a raw string as it is. If it is a raw string, we
    # interpret as the final schedule.
    try:
        config = yaml.safe_load(best_plan['config'])
        if isinstance(config, str):
            config = {"schedule": config}

        # add cal targets from linked table
        cal_keys = ['boresight', 'elevation', 'focus', 'allow_partial', 'az_speed', 'az_accel']
        config['cal_targets'] = []
        for i, source in enumerate(best_plan['cal_targets.source']):
            if source is None:
                raise ValueError("Source name is empty")
            cal_target = {}
            cal_target['source'] = source
            for cal_key in cal_keys:
                if best_plan['cal_targets.' + cal_key][i] is not None:
                    cal_target[cal_key] = best_plan['cal_targets.' + cal_key][i]
            config['cal_targets'].append(cal_target)
        logger.info(f"best plan cal targets: {config['cal_targets']}")
    except Exception as e:
        logger.error(f"Failed to load yaml config with error: {e}")
        logger.error(f"config: {best_plan['config']}")
        raise ValueError("Failed to parse yaml config")

    script_base = os.environ['SCHED_BASE']
    module_path = op.join(script_base, program) + (".py" if not program.endswith(".py") else "")

    if not op.exists(module_path):
        raise FileNotFoundError(f"Program {program} not found")

    # load module from scheduler-scripts
    # updated module will not automatically be reloaded
    # it is expected the server will restart on updating
    # schedule program scripts
    module_name = "_" + program.replace(".py", "").replace("/", ".")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    schedule = module.main(t0=t0, t1=t1, **config)

    return schedule


HANDLERS = {
    'dummy': dummy_handler,
    'rest': rest_handler,
}

def get_handler(policy_name):
    assert policy_name in HANDLERS, f"Unknown policy {policy_name}"
    return HANDLERS[policy_name]
