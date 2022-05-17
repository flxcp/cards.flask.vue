from flask_restful import Resource, fields, marshal_with, reqparse
from .Validation import BusinessValidationError, NotFoundError, PropertyExistError
from app.access import acs_card_id, acs_card_id_question, acs_deck_id, acs_user_email, acs_user_id
from app.db import db, Cards
from flask_security import current_user, auth_required
from app.cache import cache

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('deck_id')
parser.add_argument('question')
parser.add_argument('answer')
parser.add_argument('response')

response_fields = {
    "id": fields.Integer,
    "deck_id": fields.Integer,
    "question": fields.String,
    "answer": fields.String,
    "response": fields.Integer
}


class CardAPI(Resource):
    @auth_required('token')
    @marshal_with(response_fields)
    def get(self, card_id):

        card = acs_card_id(card_id, current_user.id)

        if card:
            return card
        else:
            raise NotFoundError(status_code=404)

    @auth_required('token')
    @marshal_with(response_fields)
    def post(self):
        args = parser.parse_args()
        deck_id = args.get('deck_id', None)
        question = args.get('question', None)
        answer = args.get('answer', None)
        response = (args.get('response', None) or 0)

        if deck_id is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD001', error_message='Deck User ID is required')

        if question is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD002', error_message='Question is required')

        if answer is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD003', error_message='Answer is required')

        card = acs_card_id_question(deck_id, question)

        if card:
            raise PropertyExistError(status_code=409)

        card = Cards(deck_id=deck_id, user_id=current_user.id, question=question,
                     answer=answer, response=response)

        cache.delete_memoized(acs_deck_id, deck_id, current_user.id)
        cache.delete_memoized(acs_user_email, current_user.email)
        cache.delete_memoized(acs_user_id, current_user.id)

        db.session.add(card)
        db.session.commit()

        deck = acs_deck_id(deck_id, current_user.id)
        deck.status = 0

        db.session.add(deck)
        db.session.commit()

        return card, 201

    @auth_required('token')
    @marshal_with(response_fields)
    def put(self, card_id):
        args = parser.parse_args()
        deck_id = args.get('deck_id', None)
        question = args.get('question', None)
        answer = args.get('answer', None)
        response = (args.get('response', None) or 0)

        if deck_id is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD001', error_message='Deck User ID is required')

        if question is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD002', error_message='Question is required')

        if answer is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD003', error_message='Answer is required')

        card = acs_card_id(card_id, current_user.id)

        if card is None:
            raise NotFoundError(status_code=404)

        existing_card = acs_card_id_question(deck_id, question)

        if existing_card:
            raise PropertyExistError(status_code=409)

        cache.delete_memoized(acs_card_id, card.id, current_user.id)
        cache.delete_memoized(acs_card_id_question, deck_id, question)
        cache.delete_memoized(acs_deck_id, deck_id, current_user.id)
        cache.delete_memoized(acs_user_email, current_user.email)
        cache.delete_memoized(acs_user_id, current_user.id)

        card.deck_id = deck_id
        card.question = question
        card.answer = answer
        card.response = response

        db.session.add(card)
        db.session.commit()

        deck = acs_deck_id(deck_id, current_user.id)
        deck.status = 0

        db.session.add(deck)
        db.session.commit()

        return card

    @auth_required('token')
    def delete(self, card_id):
        card = acs_card_id(card_id, current_user.id)

        if card is None:
            raise NotFoundError(status_code=404)

        cache.delete_memoized(acs_card_id, card.id, current_user.id)
        cache.delete_memoized(acs_card_id_question, card.deck_id, card.question)
        cache.delete_memoized(acs_deck_id, card.deck_id, current_user.id)
        cache.delete_memoized(acs_user_email, current_user.email)
        cache.delete_memoized(acs_user_id, current_user.id)

        db.session.delete(card)
        db.session.commit()

        return '', 200
