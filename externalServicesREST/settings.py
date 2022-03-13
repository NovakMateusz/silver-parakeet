import os


class Settings:
    def __init__(self):

        try:
            self.app_name = os.getenv('APP_NAME')
            self.api_key = os.environ['API_KEY']
            self.external_api_key = os.environ['EXTERNAL_RESOURCES_KEY']
        except KeyError as error:
            print('No environment variable: %s', error)


def load() -> Settings:
    return Settings()
