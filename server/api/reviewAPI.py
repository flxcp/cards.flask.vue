from flask_restful import Resource, fields, marshal_with, reqparse
from .Validation import NotFoundError
from app.db import db, Cards, CardResponse, LoginLedger
from app.access import acs_card_id, acs_deck_id, acs_loginledger_id, acs_user_email, acs_user_all, acs_user_id
from flask_security import auth_required, current_user
from app.cache import cache
import datetime

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('response')

response_fields = {
    "id": fields.Integer,
    "deck_id": fields.Integer,
    "question": fields.String,
    "answer": fields.String,
    "response": fields.Integer,
}


class ReviewAPI(Resource):
    @auth_required('token')
    @marshal_with(response_fields)
    def put(self, card_id, response):

        card = acs_card_id(card_id, current_user.id)

        if card is None:
            raise NotFoundError(status_code=404)

        cache.delete_memoized(acs_card_id, card_id, current_user.id)
        cache.delete_memoized(acs_deck_id, card.deck_id, current_user.id)
        cache.delete_memoized(acs_user_all)
        cache.delete_memoized(acs_user_email, current_user.email)
        cache.delete_memoized(acs_user_id, current_user.id)

        card.response = response
        db.session.add(card)
        db.session.commit()


        res = CardResponse(user_id=current_user.id, card_id=card_id,
                           response=response, deck_id=card.deck_id)

        loginledger = acs_loginledger_id(current_user.id)

        if loginledger:
            cache.delete_memoized(acs_loginledger_id, current_user.id)
            loginledger.last_active_time = datetime.datetime.now()
        else:
            loginledger = LoginLedger(
                user_id=current_user.id, last_active_time=datetime.datetime.now())

        
        db.session.add(loginledger)
        db.session.add(res)

        db.session.commit()

        status = db.session.query(Cards).filter(
            (Cards.deck_id == card.deck_id) & (Cards.response == 0)).first()

        if status is None:

            deck = acs_deck_id(card.deck_id, current_user.id)
            deck.status = 1
            deck.date = datetime.datetime.now()

            db.session.add(deck)
            db.session.commit()
        else:
            deck = acs_deck_id(card.deck_id)
            deck.date = datetime.datetime.now()

            db.session.add(deck)
            db.session.commit()

        return card
