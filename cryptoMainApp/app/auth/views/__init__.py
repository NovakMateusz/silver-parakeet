import urllib.parse

from flask import flash, render_template, redirect, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask_mail import Message
from sqlalchemy.exc import IntegrityError

from app.auth.forms import LoginForm, RegistrationForm
from app.auth import auth_blueprint
from app.auth.models import User, AccountActivationLink
from app.extensions import db, login_manager, mail
from app.trading.models import Wallet


def send_email(activation_key: str, recipient: str):
    url_prefix = request.url_root
    url_suffix = url_for('auth.account_activation_view', activation_id=activation_key)
    activation_url = urllib.parse.urljoin(url_prefix, url_suffix)
    msg = Message('Activate email', recipients=[recipient])
    msg.body = activation_url
    mail.send(msg)


@login_manager.user_loader
def load_user(user_id: int):
    if user_id is not None:
        return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login_view'))


@auth_blueprint.route('/login', methods=['POST', 'GET'])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for('pages.home_view'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(request.form.get('password')):
            if not user.is_active():
                return redirect(url_for('auth.not_active_view'))
            login_user(user)
            return redirect(url_for('pages.home_view'))
        else:
            flash('Wrong username or password')
    return render_template('login.html', form=login_form)


@auth_blueprint.route('/not-active')
def not_active_view():
    return '<h1> Your account is not active </h1>'


@auth_blueprint.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('auth.login_view'))


@auth_blueprint.route('/register', methods=['POST', 'GET'])
def register_view():
    if current_user.is_authenticated:
        return redirect(url_for('pages.home_view'))

    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            email = request.form.get('email')
            if User.query.filter_by(email=email).first():
                flash("Email already taken")
            else:
                password = request.form.get('password')
                new_user = User(username=username, email=email, password=password)
                new_link = AccountActivationLink(user=new_user)
                try:
                    db.session.add(new_user)
                    db.session.add(new_link)
                    db.session.commit()
                except IntegrityError as error:
                    flash("Internal Server Error")
                    print(error)
                else:
                    send_email(new_link.value, email)

                return redirect(url_for('auth.login_view'))
        else:
            flash("Username already taken")
    return render_template('registration.html', form=registration_form)


@auth_blueprint.route('/activate/<uuid:activation_id>')
def account_activation_view(activation_id):
    activation_link = AccountActivationLink.query.filter_by(value=str(activation_id)).one_or_none()
    if activation_link and not activation_link.user.active:
        activation_link.user.active = True
        db.session.add(activation_link)
        wallet = Wallet(inhouse_currency=0, user_id=activation_link.user.id)
        db.session.add(wallet)
        db.session.commit()

        return f'<h1> User {activation_link.user.public_id} activated </h1>'
    else:
        return '<h1> Problem </h1>'
