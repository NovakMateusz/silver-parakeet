import os


class Settings:
    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY', 'DevelopmentKey')


def load() -> Settings:
    return Settings()
