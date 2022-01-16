from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from loguru import logger

from config import config

logger.add('log/debug.log', level='DEBUG',
           format='{time} {level} {message}', rotation='10 KB', compression='zip')

db = SQLAlchemy()
jwt = JWTManager()
docs = FlaskApiSpec()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Blueprints

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    db.init_app(app)
    jwt.init_app(app)
    docs.init_app(app)

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='videoblog',
            version='v1',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()]
        ),
        'APISPEC_SWAGGER_URL': '/swagger'
    })

    return app
