from flask import flash, render_template, request
from flask_login import current_user

from app.pages import pages_blueprint
from app.pages.forms import MessageForm


@pages_blueprint.route('/')
@pages_blueprint.route('/home')
def home_view():
    return render_template('home.html')


@pages_blueprint.route('/contact', methods=['POST', 'GET'])
def contact_view():
    message_form = MessageForm()
    if current_user.is_authenticated:
        message_form.email.data = current_user.email

    if message_form.validate_on_submit():
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        message = request.form.get('message')

        # Prepare email

        flash('Email has been sent, thank you!')
        message_form.reset_fields()
    return render_template('contact.html', form=message_form)
