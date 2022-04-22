from typing import Dict

from flask import render_template, flash
from flask_login import login_required, current_user

from app.user import user_blueprint
from app.utils.prepare_data import prepare_images_links
from app.user.utils import UserDataModel, AccountBalanceModel
from app.user.forms import AccountBalanceForm
from app.extensions import db
from app.trading.models import WalletTopUp


@user_blueprint.route('/account')
@login_required
def account_view():
    user: UserDataModel = UserDataModel(current_user)
    output_model: Dict = user.extract_data()
    return render_template('account.html', images=prepare_images_links(), output=output_model)


@user_blueprint.route('/account/balance', methods=['POST', 'GET'])
@login_required
def balance_view():
    account_balance: AccountBalanceModel = AccountBalanceModel(current_user)

    account_balance_form = AccountBalanceForm()

    if account_balance_form.validate_on_submit():
        operation_type = account_balance_form.type.data
        amount = account_balance_form.amount.data

        if operation_type == 'withdraw_all':
            amount = current_user.wallet.inhouse_currency
            operation_type = 'withdraw'
            current_user.wallet.inhouse_currency = 0
            db.session.add(current_user)

        else:
            if amount <= 0:
                flash('Incorrect value')
                return render_template('balance.html', form=account_balance_form,
                                       output_model=account_balance.extract_data())

            if operation_type == 'withdraw':
                if current_user.wallet.inhouse_currency < amount:
                    flash("You don't have enough money to withdraw")
                    return render_template('balance.html', form=account_balance_form,
                                           output_model=account_balance.extract_data())

                current_user.wallet.inhouse_currency -= amount
                db.session.add(current_user)

            else:
                current_user.wallet.inhouse_currency += amount
                db.session.add(current_user)

        wallet_top_up = WalletTopUp(operation_type=operation_type, amount=amount, wallet_id=current_user.wallet.id)
        db.session.add(wallet_top_up)
        db.session.commit()

    account_balance_form.amount.data = 0.0
    account_balance_form.amount.raw_data = ['0.0']
    return render_template('balance.html', form=account_balance_form, output_model=account_balance.extract_data())
