from flask import Flask

from .extensions import db, login_manager
from settings import load


def register_blueprints(app: Flask):
    from .user.views import user_blueprint
    from .pages.views import pages_blueprint
    from .trading.views import trading_blueprint
    app.register_blueprint(pages_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(trading_blueprint)


def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)
    app_settings = load()
    app.config.from_object(app_settings)
    db.init_app(app)
    login_manager.init_app(app)
    return app
