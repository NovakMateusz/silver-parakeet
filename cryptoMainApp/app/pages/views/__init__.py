from flask import render_template

from app.pages import pages_blueprint


@pages_blueprint.route('/')
@pages_blueprint.route('/home')
def home_view():
    return render_template('home.html')


@pages_blueprint.route('/about')
def about_view():
    return render_template('about.html')


@pages_blueprint.route('/contact')
def contact_view():
    return render_template('contact.html')
