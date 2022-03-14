import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(34), unique=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    hash_password = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username: str, email: str, password: str):
        self.public_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.hash_password = generate_password_hash(password)

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    def get_public_id(self):
        return self.public_id

    def is_authenticated(self):
        return self.authenticated

    def verify_password(self, password_to_verify: str):
        return check_password_hash(self.password, password_to_verify)

    def __repr__(self):
        return f'<User {self.public_id}>'
