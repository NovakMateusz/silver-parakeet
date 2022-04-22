from typing import Dict, Set, List

from app.auth.models import User
from app.utils.constans import NAME_CODE_MAPPING


class UserDataModel:
    def __init__(self, user_model: User):
        self.user_model: User = user_model

    def _get_account_info(self) -> Dict:
        temp_dict: Dict = dict()
        temp_dict['created_at']: str = self.user_model.created_at.strftime("%m.%d.%Y %H:%M:%S")
        temp_dict['email']: str = self.user_model.email
        temp_dict['username']: str = self.user_model.username
        return temp_dict

    def _get_wallet_info(self) -> Dict:
        temp_dict: Dict = dict()
        temp_dict['in-house']: float = round(self.user_model.wallet.inhouse_currency, 3)
        temp_dict['crypto']: List = []
        all_currencies_set: Set = set(NAME_CODE_MAPPING.keys())
        for crypto in self.user_model.wallet.currencies:
            all_currencies_set.remove(crypto.currency.name)
            temp_dict['crypto'].append(
                {
                    'amount': round(crypto.amount, 3),
                    'name': crypto.currency.name,
                    'code': crypto.currency.code
                }
            )

        for crypto in all_currencies_set:
            temp_dict['crypto'].append(
                {
                    'amount': 0.0,
                    'name': crypto,
                    'code': NAME_CODE_MAPPING[crypto]
                }
            )

        return temp_dict

    def _get_transaction_history(self) -> List:
        temp_list: List = []
        for index, transaction in enumerate(self.user_model.wallet.transaction_history, start=1):
            temp_list.append(
                {
                    'id': index,
                    'amount': transaction.amount,
                    'name': transaction.currency.name,
                    'code': transaction.currency.code,
                    'price_at_transaction': transaction.current_price,
                    'transaction_date': transaction.date.strftime("%m.%d.%Y %H:%M:%S"),
                    'operation_type': transaction.operation_type,
                    'total_cost': transaction.total_cost
                }
            )
        return temp_list

    def extract_data(self) -> Dict:
        return {'user': self._get_account_info(),
                'wallet': self._get_wallet_info(),
                'transaction_history': self._get_transaction_history()
                }


class AccountBalanceModel:
    def __init__(self, user_model: User):
        self.user_model: User = user_model

    def _get_money_state(self) -> float:
        return round(self.user_model.wallet.inhouse_currency, 3)

    def _get_top_ups_history(self) -> List:
        temp_list: List = []
        for index, transaction in enumerate(self.user_model.wallet.wallet_top_up, start=1):
            temp_list.append(
                {
                    'id': index,
                    'amount': transaction.amount,
                    'transaction_date': transaction.date.strftime("%m.%d.%Y %H:%M:%S"),
                    'operation_type': transaction.operation_type,
                }
            )
        return temp_list

    def extract_data(self) -> Dict:
        return {
            'state': self._get_money_state(),
            'top_ups': self._get_top_ups_history()
        }
