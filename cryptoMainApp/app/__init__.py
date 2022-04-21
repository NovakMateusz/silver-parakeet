from pathlib import Path
from typing import Optional

from flask import Flask

from settings import Settings
from .extensions import db, login_manager, mail
from .auth.models import *
from .trading.models import *
from .utils.search import Searcher


def register_blueprints(app: Flask) -> None:
    from .auth.views import auth_blueprint
    from .pages.views import pages_blueprint
    from .trading.views import trading_blueprint
    from .user.views import user_blueprint
    app.register_blueprint(pages_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(trading_blueprint)
    app.register_blueprint(user_blueprint)


def register_extensions(app: Flask) -> None:
    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)


def create_app(app_settings: Optional[Settings] = None) -> Flask:
    template_path = Path('./templates')
    static_path = template_path / 'static'
    app = Flask(__name__, template_folder=str(template_path), static_url_path='', static_folder=str(static_path))
    if not app_settings:
        app_settings = Settings()
    app.config.from_object(app_settings)
    register_blueprints(app)
    register_extensions(app)
    app.config['searcher'] = Searcher(app_settings.REST_API_KEY, app_settings.REST_API_URL)

    return app
