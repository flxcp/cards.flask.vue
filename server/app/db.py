from math import remainder
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import datetime

Base = declarative_base()
db = SQLAlchemy()


UserRoles = db.Table('UserRoles',
                     db.Column('user_id', db.Integer(),
                               db.ForeignKey('User.id')),
                     db.Column('role_id', db.Integer(),
                               db.ForeignKey('Role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), default=True)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    userdeck = db.relationship('Deck', cascade="all, delete", lazy='subquery')
    roles = db.relationship('Role', secondary=UserRoles,
                            backref=db.backref('users', lazy='dynamic'))


class UserProfile(db.Model):
    __tablename__ = 'UserProfile'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.id'), nullable=False)
    email_format = db.Column(db.String(40), default='email', nullable=True)
    communication_preference = db.Column(
        db.String(40), default='email', nullable=True)
    webhook_url = db.Column(db.String(255), nullable=True, default=None)


class Role(db.Model, RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Deck(db.Model):
    __tablename__ = 'Deck'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.datetime.now())
    deckcards = db.relationship(
        'Cards', cascade="all, delete", lazy='subquery')


class Cards(db.Model):
    __tablename__ = 'Cards'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.id'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey(
        'Deck.id'), nullable=False)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    response = db.Column(db.Integer, nullable=False, default=0)


class CardResponse(db.Model):
    __tablename__ = 'CardResponse'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.id'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey(
        'Deck.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey(
        'Cards.id'), nullable=False)
    response = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.datetime.now())


class LoginLedger(db.Model):
    __tablename__ = 'LoginLedger'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.id'), nullable=False)
    last_active_time = db.Column(db.DateTime, nullable=False,
                                 default=datetime.datetime.now())
