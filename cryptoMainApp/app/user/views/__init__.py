from typing import Dict, List

from flask import render_template
from flask_login import login_required

from app.user import user_blueprint
from app.user.utils import prepare_items


@user_blueprint.route('/account')
@login_required
def account_view():
    elements: List[List[Dict]] = prepare_items()
    return render_template('account.html', elements=elements)
