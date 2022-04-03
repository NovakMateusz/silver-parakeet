from app.trading import trading_blueprint


@trading_blueprint.route('/trade')
def trade():
    return '<h1> trade </h1>'

