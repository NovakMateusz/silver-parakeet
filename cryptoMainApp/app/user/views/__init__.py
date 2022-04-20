from typing import Dict, List

from flask import render_template
from flask_login import login_required, current_user

from app.user import user_blueprint
from app.utils.prepare_data import prepare_items
from app.user.utils import UserDataModel, prepare_images_links


@user_blueprint.route('/account')
@login_required
def account_view():
    user: UserDataModel = UserDataModel(current_user)
    output_model: Dict = user.extract_data()
    return render_template('account.html', images=prepare_images_links(), output=output_model)
