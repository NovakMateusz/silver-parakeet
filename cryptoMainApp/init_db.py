import os

from app import create_app, db
from app.utils.constans import NAME_CODE_MAPPING


def populate_currency_table(database, currency_model):
    for name, code in NAME_CODE_MAPPING.items():
        temp_item = currency_model(name=name, code=code)
        database.session.add(temp_item)
    database.session.commit()


def create_admin_user(database, user_model):
    admin = user_model(username='Admin', email='admin@admin.com', password='admin')
    admin.active = True
    database.session.add(admin)
    database.session.commit()


def creat_wallet_for_admin(database, wallet_model):
    wallet = wallet_model(inhouse_currency=142.5, user_id=1)
    database.session.add(wallet)
    database.session.commit()


def create_wallet_entries(database, wallet_entries_model):
    wallet_item = wallet_entries_model(wallet_id=1, currency_id=12, amount=12.3)
    database.session.add(wallet_item)
    wallet_item = wallet_entries_model(wallet_id=1, currency_id=1, amount=22.3)
    database.session.add(wallet_item)
    wallet_item = wallet_entries_model(wallet_id=1, currency_id=2, amount=22.3)
    database.session.add(wallet_item)
    database.session.commit()


def create_transaction_history(database, transaction_history_model):
    item = transaction_history_model(operation_type='sell', amount=12.4, current_price=23.2, currency_id=4, wallet_id=1)
    database.session.add(item)
    item = transaction_history_model(operation_type='buy', amount=12.4, current_price=24.2, currency_id=4, wallet_id=1)
    database.session.add(item)
    item = transaction_history_model(operation_type='buy', amount=122.4, current_price=24.2, currency_id=1, wallet_id=1)
    database.session.add(item)
    item = transaction_history_model(operation_type='buy', amount=144.4, current_price=24.2, currency_id=2, wallet_id=1)
    database.session.add(item)
    item = transaction_history_model(operation_type='sell', amount=1211.4, current_price=24.2, currency_id=2, wallet_id=1)
    database.session.add(item)
    database.session.commit()


def create_top_up_history(database, wallet_top_up_model):
    item = wallet_top_up_model(operation_type='withdraw', amount=12.4, wallet_id=1)
    database.session.add(item)
    item = wallet_top_up_model(operation_type='deposit', amount=12.4, wallet_id=1)
    database.session.add(item)
    item = wallet_top_up_model(operation_type='deposit', amount=12.4, wallet_id=1)
    database.session.add(item)
    database.session.commit()


if __name__ == '__main__':
    from app.auth.models import User
    from app.trading.models import Currency, TransactionHistory, Wallet, WalletEntries, WalletTopUp
    os.environ.setdefault('MAIL_USERNAME', "tempUser")
    os.environ.setdefault('MAIL_PASSWORD', "tempPassword")
    app = create_app()
    db.create_all(app=app)
    with app.app_context():
        create_admin_user(db, User)
        populate_currency_table(db, Currency)
        creat_wallet_for_admin(db, Wallet)
        create_wallet_entries(db, WalletEntries)
        create_transaction_history(db, TransactionHistory)
        create_top_up_history(db, WalletTopUp)
