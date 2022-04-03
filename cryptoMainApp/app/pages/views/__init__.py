from app.pages import pages_blueprint


@pages_blueprint.route('/')
@pages_blueprint.route('/home')
def home_view():
    return '<h1> Home view </h1>'


@pages_blueprint.route('/about')
def about_view():
    return '<h1> About view </h1>'


@pages_blueprint.route('/contact')
def contact_view():
    return '<h1> Contact view </h1>'
