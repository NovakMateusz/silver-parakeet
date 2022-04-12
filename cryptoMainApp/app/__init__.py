from pathlib import Path
from typing import Optional


from flask import Flask

from settings import Settings
from .extensions import db, login_manager, mail


def register_blueprints(app: Flask):
    from .auth.views import auth_blueprint
    from .pages.views import pages_blueprint
    from .trading.views import trading_blueprint
    app.register_blueprint(pages_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(trading_blueprint)


def register_extensions(app: Flask):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


def create_app(app_settings: Optional[Settings] = None) -> Flask:
    template_path = Path('./templates')
    app = Flask(__name__, template_folder=str(template_path))
    if not app_settings:
        app_settings = Settings()
    app.config.from_object(app_settings)

    register_blueprints(app)
    register_extensions(app)
    return app
