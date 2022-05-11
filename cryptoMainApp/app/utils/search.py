from typing import Dict, List

import requests


class Searcher:
    NEXT_DAY_PREDICTION_ENDPOINT: str = 'next-day-prediction'
    PREDICTIONS_ENDPOINT: str = 'predictions'
    EXCHANGE_ENDPOINT: str = 'state'
    HEALTH_ENDPOINT: str = 'health'
    HISTORICAL_ENDPOINT: str = 'history'

    def __init__(self, api_key: str, base_url: str):
        self.session = requests.Session()
        self.session.headers.update({'API_KEY': api_key})
        self.base_url = base_url

    def get_next_day_prediction(self, code: str) -> float:
        params: Dict = {'code': code}
        url: str = f'{self.base_url}/{self.NEXT_DAY_PREDICTION_ENDPOINT}'
        response = self.session.get(url, params=params)
        response = response.json()
        float_response = float(response['prediction'])
        return float('{:.3f}'.format(float_response))

    def get_all_next_day_prediction(self, code_list: List[str]) -> Dict:
        response: Dict = {}
        for code in code_list:
            response[code] = {'prediction': self.get_next_day_prediction(code)}
        return response

    def get_predictions(self, code: str):
        params: Dict = {'code': code}
        url: str = f'{self.base_url}/{self.PREDICTIONS_ENDPOINT}'
        response = self.session.get(url, params=params)
        return response.json()

    def get_historical_data(self, code: str):
        params: Dict = {'code': code}
        url: str = f'{self.base_url}/{self.HISTORICAL_ENDPOINT}'
        response = self.session.get(url, params=params)
        return response.json()

    def get_all_predictions(self) -> List[Dict]:
        params: Dict = {'code': 'all'}
        url: str = f'{self.base_url}/{self.PREDICTIONS_ENDPOINT}'
        response = self.session.get(url, params=params)
        response = response.json()
        return response['predictions']

    def check_service_health(self) -> bool:
        url: str = f'{self.base_url}/{self.HEALTH_ENDPOINT}'
        response = self.session.get(url)
        if response.status_code != 200:
            return False
        return True

    def get_exchange_rate(self, code: str):
        params: Dict = {'code': code}
        url: str = f'{self.base_url}/{self.EXCHANGE_ENDPOINT}'
        response = self.session.get(url, params=params)
        response = response.json()
        return float('{:.3f}'.format(response['exchange_rate']))

    def get_all_exchange_rates(self, code_list: List[str]) -> Dict:
        response: Dict = dict()
        for code in code_list:
            response[code] = {'exchange_rate': self.get_exchange_rate(code)}
        return response
