from flask_restful import Resource, fields, marshal_with, reqparse
from .Validation import BusinessValidationError, NotFoundError, PropertyExistError
from app.db import db, Deck
from .cardAPI import response_fields as card_response_fields
from app.access import acs_deck_id, acs_deck_userid_name, acs_user_email, acs_user_id
from flask_security import current_user, auth_required
from app.cache import cache
import datetime

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('user_id')
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('status')

response_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "status": fields.Integer,
    "date": fields.DateTime(dt_format='iso8601'),
    "cards": fields.List(fields.Nested(card_response_fields), attribute='deckcards')
}


class DeckAPI(Resource):
    @auth_required('token')
    @marshal_with(response_fields)
    def get(self, deck_id):
        deck = acs_deck_id(deck_id, current_user.id)
        if deck:
            return deck
        else:
            raise NotFoundError(status_code=404)

    @auth_required('token')
    @marshal_with(response_fields)
    def post(self):
        args = parser.parse_args()
        user_id = current_user.id
        name = args.get('name', None)
        description = args.get('description', None)
        status = (args.get('status', None) or 1)

        if name is None:
            raise BusinessValidationError(
                status_code=400, error_code='DECK001', error_message='Deck Name is required')

        if description is None:
            raise BusinessValidationError(
                status_code=400, error_code='DECK002', error_message='Deck Description is required')

        deck = acs_deck_userid_name(user_id, name)

        if deck:
            raise PropertyExistError(status_code=409)

        cache.delete_memoized(acs_deck_userid_name, user_id, name)
        cache.delete_memoized(acs_user_email, current_user.email)
        cache.delete_memoized(acs_user_id, current_user.id)

        deck = Deck(user_id=user_id, name=name,
                    description=description, status=status, date=datetime.datetime.now())
        db.session.add(deck)
        db.session.commit()

        return deck, 201

    @auth_required('token')
    @marshal_with(response_fields)
    def put(self, deck_id):
        args = parser.parse_args()
        user_id = current_user.id
        name = args.get('name', None)
        description = args.get('description', None)
        status = args.get('status', None)

        if name is None:
            raise BusinessValidationError(
                status_code=400, error_code='DECK002', error_message='Deck Name is required')

        elif description is None:
            raise BusinessValidationError(
                status_code=400, error_code='DECK003', error_message='Deck Description is required')

        deck = acs_deck_id(deck_id, user_id)

        if deck is None:
            raise NotFoundError(status_code=404)

        existing_deck = acs_deck_userid_name(user_id, name)

        if existing_deck:
            raise PropertyExistError(status_code=409)

        cache.delete_memoized(acs_deck_userid_name, user_id, name)
        cache.delete_memoized(acs_deck_id, deck_id, user_id)
        cache.delete_memoized(acs_user_email, current_user.email)
        cache.delete_memoized(acs_user_id, current_user.id)

        deck.user_id = user_id
        deck.name = name
        deck.description = description
        deck.date = datetime.datetime.now()
        deck.status = status

        db.session.add(deck)
        db.session.commit()

        return deck

    @auth_required('token')
    def delete(self, deck_id):

        deck = acs_deck_id(deck_id, current_user.id)

        if deck is None:
            raise NotFoundError(status_code=404)

        cache.delete_memoized(acs_deck_userid_name, current_user.id, deck.name)
        cache.delete_memoized(acs_deck_id, deck_id, current_user.id)
        cache.delete_memoized(acs_user_email, current_user.email)
        cache.delete_memoized(acs_user_id, current_user.id)

        db.session.delete(deck)
        db.session.commit()

        return '', 200
