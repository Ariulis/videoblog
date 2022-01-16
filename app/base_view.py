from flask import jsonify
from flask_apispec.views import MethodResource

from . import logger


class BaseView(MethodResource):
    @classmethod
    def register(cls, blueprint, spec, url, endpoint_name):
        blueprint.add_url_rule(url, view_func=cls.as_view(endpoint_name))
        blueprint.register_error_handler(422, cls.handle_error)
        spec.register(cls, blueprint=blueprint.name)

    @staticmethod
    def handle_error(e):
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
