from flask import render_template
from flask_login import login_required

from app.user import user_blueprint
from app.utils.constans import NAME_CODE_MAPPING


@user_blueprint.route('/account')
@login_required
def account_view():
    temp = {key: {'state': 0.0, 'filename': f'images/logos/{key.lower()}.svg'} for (key, value) in NAME_CODE_MAPPING.items()}
    return render_template('account.html', state=temp)

