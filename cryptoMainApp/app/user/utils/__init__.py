from typing import Dict, Set, List

from app.auth.models import User
from app.trading.models import Wallet, TransactionHistory
from app.utils.constans import NAME_CODE_MAPPING


class UserDataModel:
    def __init__(self, user_model: User):
        self.user_model: User = user_model
        self.wallet_model: Wallet = user_model.wallet
        self.transaction_history_list: List[TransactionHistory] = user_model.wallet.transaction_history
        self.output: Dict = dict()

    def _get_account_info(self) -> None:
        temp_dict: Dict = dict()
        temp_dict['created_at']: str = self.user_model.created_at.strftime("%m.%d.%Y %H:%M:%S")
        temp_dict['email']: str = self.user_model.email
        temp_dict['username']: str = self.user_model.username
        self.output['user']: Dict = temp_dict

    def _get_wallet_info(self) -> None:
        temp_dict: Dict = dict()
        temp_dict['in-house']: float = round(self.wallet_model.inhouse_currency, 3)
        temp_dict['crypto']: List = []
        all_currencies_set: Set = set(NAME_CODE_MAPPING.keys())
        for crypto in self.wallet_model.currencies:
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

        self.output['wallet'] = temp_dict

    def _get_transaction_history(self) -> None:
        temp_list: List = []
        for index, transaction in enumerate(self.transaction_history_list, start=1):
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
        self.output['transaction_history']: List = temp_list

    def extract_data(self) -> Dict:
        self._get_account_info()
        self._get_wallet_info()
        self._get_transaction_history()
        return self.output



