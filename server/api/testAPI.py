from flask_restful import Resource, fields, marshal_with, reqparse
from app.jobs.tasks import dailyRemainder, monthlyMail, importDeck, exportDeck
from flask_security import current_user
from flask import current_app as app


class TestAPI(Resource):

    def get(self):

        dailyRemainder.delay()
        monthlyMail.delay()

        return {
            'status': 'success',
            'message': 'Test API'
        }
