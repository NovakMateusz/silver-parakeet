from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class MessageForm(FlaskForm):
    name = StringField('Name')
    surname = StringField('Surname')
    email = EmailField('Email', validators=[InputRequired(), Email()])
    message = TextAreaField(validators=[Length(max=512)])

    def reset_fields(self):
        self.name.data = ''
        self.surname.data = ''
        self.email.data = ''
        self.message.data = ''
