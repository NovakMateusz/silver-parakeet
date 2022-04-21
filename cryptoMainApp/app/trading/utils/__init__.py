import json
from typing import Dict, List

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
    def __init__(self, searcher: Searcher, code: str):
        self.searcher = searcher
        self.code = code

    def _get_next_day_prediction(self) -> float:
        return self.searcher.get_next_day_prediction(self.code)

    def _get_exchange_rate(self) -> float:
        return self.searcher.get_exchange_rate(self.code)

    def _get_predictions(self) -> Dict:
        return self.searcher.get_predictions(self.code)

    def prepare_data(self) -> Dict:
        output = self._get_predictions()
        temp_labels = [item.split(' ')[0] for item in output['prediction']['Close'].keys()]

        output['prediction']['labels'] = json.dumps(self._filter_predictions(temp_labels))
        output['prediction']['values'] = json.dumps(
            self._filter_predictions(list(output['prediction']['Close'].values()))
        )
        del(output['prediction']['Close'])
        output['exchange_rate'] = self._get_exchange_rate()
        output['next_day_prediction'] = self._get_next_day_prediction()
        output['filename'] = prepare_single_image_link(output['name'])
        return output

    @staticmethod
    def _filter_predictions(list_of_elements: List, max_results: int = 365):
        size = len(list_of_elements)
        if size <= max_results:
            return list_of_elements
        return list_of_elements[size - max_results:]
