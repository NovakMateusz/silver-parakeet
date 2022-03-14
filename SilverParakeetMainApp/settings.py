import os


class Settings:
    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY', 'DevelopmentKey')
        self.SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///SilverParakeet.sqlite')


def load() -> Settings:
    return Settings()
