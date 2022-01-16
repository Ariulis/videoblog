from flask import jsonify

from . import main
from .. import logger


@main.app_errorhandler(422)
def marshmallow_errors(e):
    headers = e.data.get('headers', None)
    messages = e.data.get('messages', ['Invalid request'])
    logger.warning(
        f'Invalid input parameters: {messages}')
    if headers:
        return jsonify({
            'message': messages
        }), 400, headers
    else:
        return jsonify({
            'message': messages
        }), 400
