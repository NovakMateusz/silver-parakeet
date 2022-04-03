import os

from app import create_app, db


if __name__ == '__main__':
    from app.auth.models import User
    os.environ.setdefault('MAIL_USERNAME', "tempUser")
    os.environ.setdefault('MAIL_PASSWORD', "tempPassword")
    app = create_app()
    db.create_all(app=app)
    with app.app_context():
        admin = User(username='Admin', email='admin@admin.com', password='admin')
        admin.active = True
        db.session.add(admin)
        db.session.commit()
