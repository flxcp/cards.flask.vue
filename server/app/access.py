from app.db import db, Deck, Cards, User, UserProfile, LoginLedger
from flask_security import current_user
from app.cache import cache


@cache.memoize()
def acs_deck_id(id, user_id):
    deck = db.session.query(Deck).filter(
        (Deck.user_id == user_id) & (Deck.id == id)).first()
    return deck


@cache.memoize()
def acs_deck_userid_name(user_id, name):
    deck = db.session.query(Deck).filter(
        (Deck.user_id == user_id) & (Deck.name == name)).first()
    return deck


@cache.memoize()
def acs_card_id(id, user_id):
    card = db.session.query(Cards).filter(
        (Cards.user_id == user_id) & (Cards.id == id)).first()
    return card


@cache.memoize()
def acs_card_id_question(id, question):
    card = db.session.query(Cards).filter((Cards.deck_id == id) &
                                          (Cards.question == question)).first()
    return card


@cache.memoize()
def acs_userprofile_userid(user_id):
    userprof = db.session.query(UserProfile).filter_by(
        user_id=user_id).first()
    return userprof


@cache.memoize()
def acs_user_id(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user


@cache.memoize()
def acs_user_email(email):
    user = db.session.query(User).filter_by(email=email).first()
    return user


@cache.memoize()
def acs_user_all():
    user = db.session.query(User).all()
    return user


@cache.memoize()
def acs_loginledger_id(id):
    user = db.session.query(LoginLedger).filter_by(user_id=id).first()
    return user
