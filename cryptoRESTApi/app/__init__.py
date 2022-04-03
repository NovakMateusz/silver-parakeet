from typing import Optional

from sanic import Sanic, Blueprint
import json_logging

from settings import Settings
from app.utils.listeners import init_aiohttp_session, load_models, init_aiocache


def init_json_logging(app: Sanic):
    json_logging.init_sanic(enable_json=True)
    json_logging.init_request_instrument(app)


def register_blueprints(app: Sanic):
    from app.health.views import health_blueprint
    from app.forecast.views import forecast_blueprint
    blueprints_group = Blueprint.group(health_blueprint, forecast_blueprint, version='v1')
    app.blueprint(blueprints_group)


def create_app(app_settings: Optional[Settings] = None) -> Sanic:
    if not app_settings:
        app_settings = Settings()
    app = Sanic(app_settings.APP_NAME)
    app.update_config(app_settings)
    register_blueprints(app)
    app.register_listener(init_aiohttp_session, 'after_server_start')
    app.register_listener(load_models, 'after_server_start')
    app.register_listener(init_aiocache, 'after_server_start')
    return app
