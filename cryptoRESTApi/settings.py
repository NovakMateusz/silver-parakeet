import os


class Settings:
    def __init__(self):
        self.APP_NAME = os.environ.get('APP_NAME')
        self.API_KEY = os.environ.get('API_KEY')
        self.EXTERNAL_RESOURCES_KEY = os.environ.get('EXTERNAL_RESOURCES_KEY')
        self.EXTERNAL_RESOURCES_URL = os.environ.get('EXTERNAL_RESOURCES_URL', 'https://www.alphavantage.co/query')
        self.DROPBOX_API_KEY = os.environ.get('DROPBOX_API_KEY')
        models_directory = os.environ.get('MODELS_DIRECTORY', '/forecastingModels')
        models_hash = os.environ.get('MODELS_HASH', '08320e1e-5f92-4a22-b371-46e5928d8673')
        self.MODELS_PATH = f'{models_directory}/{models_hash}.pickle'
