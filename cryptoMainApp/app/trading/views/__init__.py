from typing import Dict, List

from flask import render_template, current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from app.extensions import db
from app.trading import trading_blueprint
from app.trading.utils import OverviewDataModel, CurrencyDataModel
from app.trading.forms import TransactionForm
from app.trading.models import TransactionHistory, WalletEntries, Currency


@trading_blueprint.route('/')
@login_required
def overview_view():
    searcher = current_app.config['searcher']
    overview = OverviewDataModel(searcher)
    output_model: List[Dict] = overview.prepare_data()
    return render_template('overview.html', output_model=output_model)


@trading_blueprint.route('/incorrect-code')
@login_required
def incorrect_code_view():
    return render_template('wrong_code.html')


@trading_blueprint.route('/<string:code>', methods=['POST', 'GET'])
@login_required
def currency_info_view(code: str):
    # TO REFORMAT
    searcher = current_app.config['searcher']
    currency_model = CurrencyDataModel(searcher, code)
    output_model: Dict = currency_model.prepare_data()

    user = current_user
    wallet = user.wallet
    code = output_model['code']
    currency = Currency.query.filter_by(code=code).first()
    wallet_entries = WalletEntries.query.filter_by(wallet_id=wallet.id).filter_by(currency_id=currency.id).first()
    if wallet_entries:
        output_model['own_coins'] = wallet_entries.amount
    else:
        output_model['own_coins'] = 0

    transaction_form = TransactionForm()
    transaction_form.name.data = output_model['name']
    transaction_form.code.data = output_model['code']
    transaction_form.price.data = output_model['exchange_rate']

    if transaction_form.validate_on_submit():
        exchange_rate = output_model['exchange_rate']
        amount = transaction_form.amount.data
        operation_type = transaction_form.type.data

        total_cost = exchange_rate * amount

        if amount <= 0:
            flash("Incorrect value.")
            return render_template('currency_info.html', output_model=output_model, form=transaction_form)

        if operation_type == 'buy':

            if wallet.inhouse_currency < total_cost:
                flash("Not enough money to buy %f coins. Top-up your wallet." % amount)
                return render_template('currency_info.html', output_model=output_model, form=transaction_form)

            wallet.inhouse_currency -= total_cost  # 1

            if not wallet_entries:
                wallet_entries = WalletEntries(wallet_id=wallet.id, currency_id=currency.id, amount=0.0)

            wallet_entries.amount += amount

        else:
            if not wallet_entries or wallet_entries.amount < amount:
                flash("You do not enough coins.")
                return render_template('currency_info.html', output_model=output_model, form=transaction_form)

            wallet.inhouse_currency += total_cost
            wallet_entries.amount -= amount

        transaction_history = TransactionHistory(operation_type=operation_type,
                                                 amount=amount,
                                                 current_price=exchange_rate,
                                                 wallet_id=wallet.id,
                                                 currency_id=currency.id)

        db.session.add(transaction_history)
        db.session.add(wallet_entries)
        db.session.add(wallet)
        db.session.commit()
        output_model['own_coins'] = wallet_entries.amount
        transaction_form.amount.data = 0

    else:
        transaction_form.amount.data = 0.0
    return render_template('currency_info.html', output_model=output_model, form=transaction_form)
