from flask import render_template

from app.user.forms import LoginForm, RegistrationForm
from app.user import user_blueprint


@user_blueprint.route('/login', methods=['POST', 'GET'])
def login_view():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)


@user_blueprint.route('/logout')
def logout_view():
    return "<h1> Logout view </h1>"


@user_blueprint.route('/register', methods=['POST', 'GET'])
def register_view():
    registration_form = RegistrationForm()
    return render_template('registration.html', form=registration_form)


@user_blueprint.route('/<uuid:public_id>')
def account_view(public_id):
    return f'<h1> Account public id: {public_id} view </h1>'
