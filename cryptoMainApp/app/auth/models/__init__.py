from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
<<<<<<< Updated upstream
# from app.trading.models import TransactionHistory, Currency
=======
>>>>>>> Stashed changes


def get_uuid() -> str:
    return str(uuid.uuid4())


<<<<<<< Updated upstream
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(34), unique=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    hash_password = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    link = db.relationship('AccountActivationLink',  uselist=False, backref='user')
    # transaction_history = db.relationship('TransactionHistory', backref='user')
    wallet = db.relationship('Wallet',  uselist=False, backref='user')

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
        return check_password_hash(self.hash_password, password_to_verify)

    def __repr__(self):
        return f'<User {self.public_id}>'


class AccountActivationLink(db.Model):
    __tablename__ = 'activation_activation_link'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(34), unique=True, default=get_uuid)
    sent = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
=======
from sqlmodel import Field, SQLModel, UniqueConstraint


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("public_id"),
                      UniqueConstraint("username"),
                      UniqueConstraint("username")
                      )
    id: int = Field(default=None, primary_key=True)
    public_id: str = Field(max_length=34)
    username: str = Field(max_length=64)
    email: str = Field(max_length=64)
    hash_password: str = Field(max_length=64)
    active: bool = Field(default=False)
    authenticated: bool = Field(default=False)
    created_at


# class User(db.Model):
#     __tablename__ = 'user'
#
#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String(34), unique=True)
#     username = db.Column(db.String(64), unique=True)
#     email = db.Column(db.String(64), unique=True)
#     hash_password = db.Column(db.String(64))
#     active = db.Column(db.Boolean, default=False)
#     authenticated = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.now)
#     link = db.relationship('AccountActivationLink', uselist=False, backref="user")
#
#     def __init__(self, username: str, email: str, password: str):
#         self.public_id = str(uuid.uuid4())
#         self.username = username
#         self.email = email
#         self.hash_password = generate_password_hash(password)
#
#     def is_active(self):
#         return self.active
#
#     def get_id(self):
#         return self.id
#
#     def get_public_id(self):
#         return self.public_id
#
#     def is_authenticated(self):
#         return self.authenticated
#
#     def verify_password(self, password_to_verify: str):
#         return check_password_hash(self.hash_password, password_to_verify)
#
#     def __repr__(self):
#         return f'<User {self.public_id}>'


# class AccountActivationLink(db.Model):
#     __tablename__ = 'activation_activation_link'
#
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.String(34), unique=True, default=get_uuid)
#     sent = db.Column(db.Boolean, default=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
>>>>>>> Stashed changes


