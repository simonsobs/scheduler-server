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

    # identify the plan that is currently active
    active_plan = None
    for plan in plans:
        t_beg = datetime.fromisoformat(plan['from'])
        t_end = datetime.fromisoformat(plan['to'])

        if t_beg <= t0 <= t_end and plan['status'] == 'active':
            active_plan = plan
            t1 = min(t1, t_end)
            break

    if active_plan is None:
        raise ValueError("No active plan found")
    
    logger.info(f"Active plan: {active_plan}")
    program = active_plan['program']

    # if active_plan['config'] is a yaml string, load it,
    # otherwise pass it as is as config string
    try:
        config = yaml.safe_load(active_plan['config'])
    except Exception as e:
        logger.warning(f"Failed to load yaml config: {e}, passing it as string")
        config = {'config': active_plan['config']}

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

    schedule = module.main(t0, t1, **config)

    return schedule


HANDLERS = {
    'dummy': dummy_handler,
    'rest': rest_handler,
}

def get_handler(policy_name):
    assert policy_name in HANDLERS, f"Unknown policy {policy_name}"
    return HANDLERS[policy_name]
