from flask import Blueprint


trading_blueprint = Blueprint('trading',  __name__, template_folder='templates', url_prefix='/trade')
