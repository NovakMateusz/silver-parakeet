from flask import render_template, redirect, request, url_for
from flask_login import login_required, logout_user, current_user, login_user

from app.user.forms import LoginForm, RegistrationForm
from app.user import user_blueprint
from app.user.models import User, AccountActivationLink
from app.extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id: int):
    if user_id is not None:
        return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('user.login_view'))


@user_blueprint.route('/login', methods=['POST', 'GET'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home_view'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(request.form.get('password')):
            if not user.is_active():
                return redirect(url_for('user.not_active_view'))
            login_user(user)
            return redirect(url_for('home_blueprint.home_view'))
        else:
            print('No user')
    return render_template('login.html', form=login_form)


@user_blueprint.route('/not-active')
def not_active_view():
    return '<h1> Your account is not active </h1>'


@user_blueprint.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('user.login_view'))


@user_blueprint.route('/register', methods=['POST', 'GET'])
def register_view():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home_view'))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            email = request.form.get('email')
            password = request.form.get('password')
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            new_link = AccountActivationLink(user=new_user)
            db.session.add(new_link)
            db.session.commit()
            return redirect(url_for('user.login_view'))
    return render_template('registration.html', form=registration_form)


@user_blueprint.route('/activate/<uuid:activation_id>')
def account_activation_view(activation_id):
    activation_link = AccountActivationLink.query.filter_by(value=str(activation_id)).one_or_none()
    if activation_link and not activation_link.user.active:
        activation_link.user.active = True
        db.session.add(activation_link)
        db.session.commit()
        return f'<h1> User {activation_link.user.public_id} activated </h1>'
    else:
        return '<h1> Problem </h1>'
