from app import create_app, db


if __name__ == '__main__':
    from app.auth.models import User, AccountActivationLink
    app = create_app()
    db.create_all(app=app)
    with app.app_context():
        admin = User(username='Admin', email='admin@admin.com', password='admin')
        admin.active = True
        temp_user = User(username='temp', email='temp@temp.com', password='temp')
        db.session.add(admin)
        db.session.add(temp_user)
        db.session.commit()
