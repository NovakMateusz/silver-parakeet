import json
from typing import Dict, List, Optional

from app.utils.search import Searcher
from app.utils.constans import CODE_NAME_MAPPING, NAME_CODE_MAPPING
from app.utils.prepare_data import prepare_images_links, prepare_single_image_link


class OverviewDataModel:
    def __init__(self, searcher: Searcher):
        self.searcher = searcher

    def _get_next_day_predictions(self):
        return self.searcher.get_all_next_day_prediction(CODE_NAME_MAPPING.keys())

    def _get_all_exchange_rates(self):
        return self.searcher.get_all_exchange_rates(CODE_NAME_MAPPING.keys())

    def prepare_data(self) -> List[Dict]:
        all_exchange_rates = self._get_all_exchange_rates()
        all_next_day_predictions = self._get_next_day_predictions()
        files = prepare_images_links()
        result: List[Dict] = []
        for name, code in NAME_CODE_MAPPING.items():
            result.append(
                {
                    'name': name,
                    'code': code,
                    'exchange_rate': all_exchange_rates[code]['exchange_rate'],
                    'prediction': all_next_day_predictions[code]['prediction'],
                    'filename': files[name]
                }
            )
        return result


class CurrencyDataModel:
    def __init__(self, searcher: Searcher, code: str, return_predictions: int = 30):
        self.searcher = searcher
        if code not in CODE_NAME_MAPPING.keys():
            raise TypeError('Code %s is unsupported' % code)
        self.code = code
        self.return_predictions: int = return_predictions

    def _get_next_day_prediction(self) -> float:
        return self.searcher.get_next_day_prediction(self.code)

    def _get_exchange_rate(self) -> float:
        return self.searcher.get_exchange_rate(self.code)

    def _get_predictions(self) -> Dict:
        return self.searcher.get_predictions(self.code)

    def _get_historical_data(self) -> Dict:
        return self.searcher.get_historical_data(self.code)

    def prepare_data(self) -> Dict:
        output: Dict = {'chart': {}}

        predictions: Dict = self._get_predictions()
        predictions_items: Dict = predictions['prediction']['Close']
        predictions_sorted_keys = sorted(predictions_items.keys())

        output['name'] = predictions['name']
        output['code'] = predictions['code']

        history_data: Dict = self._get_historical_data()
        history_data_items: Dict = history_data['history']['Price']

        common_keys = sorted(set(predictions_sorted_keys).intersection(set(history_data_items.keys())))
        last_common_key = common_keys[-1]
        last_common_key_index = predictions_sorted_keys.index(last_common_key) + 1
        predictions_keys = common_keys + predictions_sorted_keys[last_common_key_index: last_common_key_index + self.return_predictions]

        history_data_values = [history_data_items.get(index) for index in common_keys]

        predictions_values = [predictions_items[index] for index in predictions_keys]

        output['chart']['labels'] = predictions_keys
        output['chart']['predictions'] = predictions_values
        output['chart']['history'] = history_data_values
        output['exchange_rate'] = self._get_exchange_rate()
        output['next_day_prediction'] = self._get_next_day_prediction()
        output['filename'] = prepare_single_image_link(output['name'])
        return output

    @staticmethod
    def _filter_predictions(list_of_elements: List, max_results: int = 200):
        size = len(list_of_elements)
        if size <= max_results:
            return list_of_elements
        return list_of_elements[size - max_results:]
