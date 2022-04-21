from datetime import datetime

from app.extensions import db
from app.utils.constans import ALLOWED_OPERATION_TYPES


__all__ = ['Currency', 'TransactionHistory', 'Wallet', 'WalletEntries', 'WalletTopUp']


class WalletEntries(db.Model):
    __tablename__ = 'wallet_entries'

    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), primary_key=True)
    amount = db.Column(db.Float)

    currency = db.relationship('Currency')


class Wallet(db.Model):
    __tablename__ = 'wallet'

    id = db.Column(db.Integer, primary_key=True)
    inhouse_currency = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    transaction_history = db.relationship('TransactionHistory', backref='wallet')
    wallet_top_up = db.relationship('WalletTopUp', backref='wallet')
    currencies = db.relationship('WalletEntries')


class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    code = db.Column(db.String(6), unique=True)

    transaction_history = db.relationship('TransactionHistory', backref='currency', uselist=False)


class WalletTopUp(db.Model):
    __tablename__ = 'wallet_top_up'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    amount = db.Column(db.Float)

    waller_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))


class TransactionHistory(db.Model):
    __tablename__ = 'transaction_history'

    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.String(6))
    date = db.Column(db.DateTime, default=datetime.now)
    amount = db.Column(db.Float)
    current_price = db.Column(db.Float)
    total_cost = db.Column(db.Float)

    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))

    def __init__(self, operation_type: str, amount: float, current_price: float, currency_id: int, wallet_id: int):
        operation = operation_type.lower()
        self.operation_type = operation if operation in ALLOWED_OPERATION_TYPES \
            else self._raise(AttributeError('Unallowed operation type %s' % operation_type))

        self.amount = amount if amount > 0 \
            else self._raise(AttributeError('Value %f can not be less then 0 ' % operation_type))

        self.current_price = current_price if current_price > 0 \
            else self._raise(AttributeError('Value %f can not be less then 0 ' % current_price))

        self.total_cost = self.amount * current_price
        self.currency_id = currency_id
        self.wallet_id = wallet_id

    @staticmethod
    def _raise(exception: Exception): raise exception
