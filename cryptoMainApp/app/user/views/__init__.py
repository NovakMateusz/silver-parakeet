from typing import Dict, List

from flask import render_template
from flask_login import login_required

from app.user import user_blueprint
from app.utils.constans import NAME_CODE_MAPPING


def chunks(items: List, n: int = 5):
    for i in range(0, len(items), n):
        yield items[i:i + n]


def prepare_items() -> List[List[Dict]]:
    items: List[Dict] = [{'name': key, 'state': 0.0, 'filename': f'images/logos/{key.lower()}.svg'} for key in NAME_CODE_MAPPING.keys()]
    result: List[List[Dict]] = []
    for item in chunks(items):
        result.append(item)
    return result


@user_blueprint.route('/account')
@login_required
def account_view():
    elements: List[List[Dict]] = prepare_items()
    return render_template('account.html', elements=elements)
