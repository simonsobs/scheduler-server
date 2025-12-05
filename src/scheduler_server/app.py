"""Create a dummy server for testing purposes."""

import os
import flask
import flask_cors
from datetime import datetime, timezone
import json
import traceback
import dotenv
dotenv.load_dotenv()

from . import handler, utils

import logging
logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)

# Allow CORS for all domains.
flask_cors.CORS(app)

@app.route('/api/v1/schedule/', methods=['POST'])
def schedule():
    """return a schedule"""
    data = flask.request.get_json()
    app.logger.debug(f"Processing request: {data}")

    # check for missing field
    for f in ['t0', 't1', 'policy']:
        if f not in data:
            response = flask.jsonify({
                'status': 'error',
                'message': f'Missing {f} field'
            })
            response.status_code = 400
            return response

    t0 = data['t0']
    t1 = data['t1']
    policy = data['policy']

    # parse into datetime objects
    try:
        t0 = datetime.fromisoformat(t0)
        t1 = datetime.fromisoformat(t1)
        # if no timezone is specified, assume UTC
        if t0.tzinfo is None:
            t0 = t0.replace(tzinfo=timezone.utc)
        if t1.tzinfo is None:
            t1 = t1.replace(tzinfo=timezone.utc)
    except ValueError:
        response = flask.jsonify({
            'status': 'error',
            'message': 'Invalid date format, needs to be ISO format'
        })
        response.status_code = 400
        return response

    # policy is a json string, so parse it now. The json
    # has the form {"policy": "name", "preset": "preset_name", "config": {...}, }
    # preset represents a predefined set of config values which will be merged
    # with the user config. If no preset is specified, the policy name is used.

    try:
        policy_dict = json.loads(policy)
    except json.JSONDecodeError:
        response = flask.jsonify({
            'status': 'error',
            'message': 'Invalid policy, needs to be a json string'
        })
        response.status_code = 400
        return response

    policy_name = policy_dict.get('policy', 'dummy')
    user_policy_config = policy_dict.get('config', {})

    # find if any config preset is specified
    config_preset_name = policy_dict.get('preset', None)

    # check policy is supported
    if policy_name not in handler.HANDLERS:
        response = flask.jsonify({
            'status': 'error',
            'message': f'Unsupported policy {policy_name}'
        })
        response.status_code = 400
        return response

    try:
        # load policy config preset and merge with user config
        if config_preset_name is None:
            policy_config = user_policy_config
        else:
            policy_config = get_preset_config(config_preset_name)
            utils.nested_update(policy_config, user_policy_config, new_keys_allowed=True)

        # get scheduler commands
        commands = handler.get_handler(policy_name)(t0, t1, policy_config)

    except Exception as e:
        response = flask.jsonify({
            'status': 'error',
            'message': f'Error: {e}'
        })
        response.status_code = 500
        app.logger.error(traceback.format_exc())
        return response

    response = flask.jsonify({
        'status': 'ok',
        'commands': commands,
        'message': 'Success'
    })
    response.status_code = 200
    return response

def get_preset_config(preset_name, default={}):
    presets = {
        'rest.satp1': {
            'program': f"scheduler-scripts/sat/gen_schedule",
            'config_path': "/scheduler-configs/sat/run_satp1.yaml",
        },
        'rest.satp2': {
            'program': "scheduler-scripts/sat/gen_schedule",
            'config_path': "scheduler-configs/sat/run_satp2.yaml",
        },
        'rest.satp3': {
            'program': "scheduler-scripts/sat/gen_schedule",
            'config_path': "scheduler-configs/sat/run_satp3.yaml",
        },
        'rest.lat': {
            'program': "scheduler-scripts/lat/gen_schedule",
            'config_path': "scheduler-configs/lat/run_lat.yaml",
        }
    }
    return presets.get(preset_name, default)
