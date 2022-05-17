from flask_restful import Resource, fields, marshal_with, reqparse
from .Validation import BusinessValidationError, NotFoundError
from app.access import acs_userprofile_userid, acs_user_id, acs_user_email
from .deckAPI import response_fields as deck_response_fields
from app.db import db
from flask_security import auth_required, current_user, admin_change_password
from app.cache import cache

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('webhook_url')
parser.add_argument('email_format')
parser.add_argument('communication_preference')

response_fields = {
    "id": fields.Integer,
    "email_format": fields.String,
    "webhook_url": fields.String,
    "communication_preference": fields.String,
}

user_response_fields = {
    "decks": fields.List(fields.Nested(deck_response_fields), attribute='userdeck')
}


class UserAPI(Resource):
    @auth_required('token')
    @marshal_with(response_fields)
    def get(self):

        user = acs_userprofile_userid(current_user.id)

        if user:
            return user
        else:
            raise NotFoundError(status_code=404)

    @auth_required('token')
    @marshal_with(response_fields)
    def put(self):
        args = parser.parse_args()
        email_format = args.get('email_format', 'email')
        communication_preference = args.get(
            'communication_preference', 'email')
        webhook_url = args.get('webhook_url', None)

        if email_format is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', error_message='Email Format is required')

        if communication_preference is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', error_message='Communication Preference is required')

        if communication_preference == 'chat' and webhook_url is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', error_message='Webhook URL is required')

        user = acs_userprofile_userid(current_user.id)

        if user is None:
            raise NotFoundError(status_code=404)

        cache.delete_memoized(acs_userprofile_userid, current_user.id)

        user.email_format = email_format
        user.communication_preference = communication_preference
        user.webhook_url = webhook_url

        db.session.add(user)
        db.session.commit()

        return user


class UpdateEmailAPI(Resource):
    @auth_required('token')
    def put(self):
        args = parser.parse_args()
        email = args.get('email', None)

        if email is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', error_message='Email is required')

        user = acs_user_id(current_user.id)

        if user is None:
            raise NotFoundError(status_code=404)

        cache.delete_memoized(acs_user_id, current_user.id)
        cache.delete_memoized(acs_user_email, current_user.email)

        user.email = email

        db.session.add(user)
        db.session.commit()

        return '', 201


class UpdatePasswordAPI(Resource):
    @auth_required('token')
    def put(self):
        args = parser.parse_args()
        password = args.get('password', None)

        if password is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', error_message='Password is required')

        user = acs_user_id(current_user.id)

        if user is None:
            raise NotFoundError(status_code=404)

        cache.delete_memoized(acs_user_id, current_user.id)
        cache.delete_memoized(acs_user_email, current_user.email)

        admin_change_password(user, password, notify=False)
        db.session.commit()

        return '', 201


class GetAllDecks(Resource):
    @auth_required('token')
    @marshal_with(user_response_fields)
    def get(self):

        user = acs_user_id(current_user.id)

        if user is None:
            raise NotFoundError(status_code=404)

        return user
