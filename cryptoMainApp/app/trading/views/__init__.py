from typing import Dict, List

from flask import render_template, redirect, url_for
from flask_login import login_required

from app.trading import trading_blueprint
from app.utils.prepare_data import prepare_items
from app.utils.constans import CODE_NAME_MAPPING


@trading_blueprint.route('/')
@login_required
def overview_view():
    elements: List[List[Dict]] = prepare_items()
    return render_template('overview.html', elements=elements)


@trading_blueprint.route('/incorrect-code')
@login_required
def incorrect_code_view():
    return render_template('wrong_code.html')


@trading_blueprint.route('/<string:code>')
@login_required
def currency_info_view(code: str):
    if code.upper() not in CODE_NAME_MAPPING.keys():
        return redirect(url_for('trading.incorrect_code_view'))
    return render_template('currency_info.html')


@trading_blueprint.route('/<string:code>/buy')
@login_required
def buy_currency_view(code: str):
    if code.upper() not in CODE_NAME_MAPPING.keys():
        return redirect(url_for('trading.incorrect_code_view'))
    return render_template('currency_info.html')


@trading_blueprint.route('/<string:code>/sell')
@login_required
def sell_currency_view(code: str):
    if code.upper() not in CODE_NAME_MAPPING.keys():
        return redirect(url_for('trading.incorrect_code_view'))
    return render_template('currency_info.html')
