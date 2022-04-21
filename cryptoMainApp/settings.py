import os


class Settings:
    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY', 'DevelopmentKey')

        self.SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///SilverParakeet.sqlite')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        self.MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
        self.MAIL_PORT = os.environ.get('MAIL_PORT', 465)
        self.MAIL_USE_SSL = bool(os.environ.get('MAIL_USE_SSL', True))
        self.MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        if not self.MAIL_USERNAME:
            raise AttributeError('Missing MAIL_USERNAME value')
        self.MAIL_DEFAULT_SENDER = self.MAIL_USERNAME
        self.MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        if not self.MAIL_PASSWORD:
            raise AttributeError('Missing MAIL_PASSWORD value')

        self.REST_API_KEY = os.environ.get('REST_API_KEY')
        self.REST_API_URL = os.environ.get('REST_API_URL', 'http://localhost:5000/v1')
