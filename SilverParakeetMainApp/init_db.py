from app import create_app, db


if __name__ == '__main__':
    from app.user.models import User
    db.create_all(app=create_app())
