from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, RadioField
from wtforms.validators import InputRequired


class TransactionForm(FlaskForm):
    name = StringField('Name')
    code = StringField('Code')
    amount = FloatField('Amount', validators=[InputRequired()])
    price = FloatField('Price')
    type = RadioField('Transaction', choices=[('sell', 'Sell'), ('buy', 'Buy')], default='buy')


