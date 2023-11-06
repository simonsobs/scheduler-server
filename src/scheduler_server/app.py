"""Create a dummy server for testing purposes."""

import os
import flask
import flask_cors
from datetime import datetime, timezone
import json
import traceback

from . import handler, utils
from .configs import get_config

import logging
logging.basicConfig(level=logging.DEBUG)

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
    # has the form {"policy": "name", "preset": "config_preset_name", "config": {...}, }
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
    # unless specified, use policy_name to find default config for policy
    config_preset_name = policy_dict.get('preset', policy_name)

    # check policy is supported
    if policy_name not in handler.HANDLERS:
        response = flask.jsonify({
            'status': 'error',
            'message': f'Invalid policy {policy_name}'
        })
        response.status_code = 400
        return response

    try:
        # load policy config preset and merge with user config
        policy_config = get_config(config_preset_name)
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