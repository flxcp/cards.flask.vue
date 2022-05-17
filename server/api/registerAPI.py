from flask_restful import Resource, reqparse
from .Validation import BusinessValidationError, PropertyExistError
from app.security import user_datastore
from app.access import acs_user_email
from app.cache import cache
from flask_security import hash_password
from app.db import db, UserProfile

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('email')
parser.add_argument('password')


class RegisterAPI(Resource):
    def post(self):
        args = parser.parse_args()
        email = args.get('email', None)
        password = args.get('password', None)

        if email is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', error_message='Email is required')

        if password is None:
            raise BusinessValidationError(
                status_code=400, error_code='USER00', error_message='Password is required')

        user = acs_user_email(email)

        if user:
            raise PropertyExistError(status_code=409)

        cache.delete_memoized(acs_user_email, email)

        user_datastore.create_user(
            email=email, password=hash_password(password))
        db.session.commit()

        user = acs_user_email(email)

        db.session.add(UserProfile(user_id=user.id))
        db.session.commit()

        return '', 201
