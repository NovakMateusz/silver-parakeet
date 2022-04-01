from sanic import Sanic
import json_logging

from settings import load
from app.utils.listeners import init_aiohttp_session


def init_json_logging(app: Sanic):
    json_logging.init_sanic(enable_json=True)
    json_logging.init_request_instrument(app)


def register_blueprints(app: Sanic):
    from app.health.views import health_blueprint
    app.blueprint(health_blueprint)


def create_app() -> Sanic:
    app_settings = load()
    app = Sanic(app_settings.app_name)

    register_blueprints(app)
    app.register_listener(init_aiohttp_session, 'after_server_start')

    return app
