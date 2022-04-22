from flask_wtf import FlaskForm
from wtforms import FloatField, RadioField, StringField
from wtforms.validators import InputRequired


class AccountBalanceForm(FlaskForm):
    card_number = StringField('Card number')
    amount = FloatField('Amount', validators=[InputRequired()])
    cvc_number = StringField('CVC')
    type = RadioField('Transaction', choices=[
        ('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('withdraw_all', 'Withdraw all')
    ], default='deposit')
