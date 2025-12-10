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
    config_path = policy_config.pop("config_path")
    program = policy_config.pop('program')

    config_base = os.environ['SCHED_CFG_DIR']
    script_base = os.environ['SCHED_SCRIPTS_DIR']

    try:
        config = yaml.safe_load(op.join(config_base, config_path))
    except:
        raise ValueError(f"Failed to parse yaml config {config_path}: {e}")

    # merge user config into loaded config
    config = {**config, **policy_config}

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

    config['t0'] = t0
    config['t1'] = t1

    schedule = module.main(**config)

    return schedule


HANDLERS = {
    'dummy': dummy_handler,
    'rest': rest_handler,
}

def get_handler(policy_name):
    assert policy_name in HANDLERS, f"Unknown policy {policy_name}"
    return HANDLERS[policy_name]
