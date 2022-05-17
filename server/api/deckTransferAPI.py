from flask_restful import Resource, marshal_with
from .Validation import BusinessValidationError, NotFoundError
from app.access import acs_deck_id, acs_card_id_question, acs_user_email, acs_user_id
from flask_security import auth_required, current_user
from flask import current_app as app, send_file, request, jsonify, url_for
from app.db import db, Cards
from .deckAPI import response_fields
from app.cache import cache
from app.jobs.tasks import importDeck, exportDeck
import datetime
import csv


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['csv']


class DeckExport(Resource):

    @auth_required('token')
    def get(self, deck_id):

        deck = acs_deck_id(deck_id, current_user.id)

        if not deck:
            raise BusinessValidationError(
                status_code=404, error_code='TRANSFER00', error_message='Deck not found')

        file_location = f'{app.config["UPLOAD_FOLDER"]}/deck_export_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}_{deck_id}.csv'

        export_file = open(file_location, 'w')
        writer = csv.writer(export_file)

        for card in deck.deckcards:
            writer.writerow([card.question, card.answer])

        export_file.close()

        return send_file(file_location, as_attachment=True)


class DeckImport(Resource):

    @marshal_with(response_fields)
    @auth_required('token')
    def post(self, deck_id):

        csv_file = request.files["file"]

        if not csv_file.filename or not allowed_file(csv_file.filename):
            raise BusinessValidationError(
                status_code=400, error_code='TRANSFER00', error_message='Cards CSV File is required is required')

        deck = acs_deck_id(deck_id, current_user.id)

        if deck is None:
            raise NotFoundError(status_code=404)

        cache.delete_memoized(acs_deck_id, deck_id, current_user.id)
        cache.delete_memoized(acs_user_email, current_user.email)
        cache.delete_memoized(acs_user_id, current_user.id)

        csv_file.save(f'{app.config["UPLOAD_FOLDER"]}file.csv')
        cards = csv.reader(
            open(f'{app.config["UPLOAD_FOLDER"]}file.csv', 'r'))

        for card in cards:
            existing_card = acs_card_id_question(deck_id, card[0])

            if not existing_card:
                db.session.add(Cards(user_id=current_user.id,
                               deck_id=deck_id, question=card[0], answer=card[1]))

        db.session.commit()

        decks = acs_deck_id(deck_id, current_user.id)
        return decks


class DeckBatchImport(Resource):

    @auth_required('token')
    def post(self, deck_id):

        csv_file = request.files["file"]

        if not csv_file.filename or not allowed_file(csv_file.filename):
            raise BusinessValidationError(
                status_code=400, error_code='TRANSFER00', error_message='Cards CSV File is required is required')

        deck = acs_deck_id(deck_id, current_user.id)

        if deck is None:
            raise NotFoundError(status_code=404)

        csv_file.save(f'{app.config["UPLOAD_FOLDER"]}file.csv')
        importDeck.delay(deck_id, current_user.id, current_user.email)

        return '', 201


class DeckBatchExport(Resource):

    @auth_required('token')
    def get(self, deck_id):

        deck = acs_deck_id(deck_id, current_user.id)

        if not deck:
            raise BusinessValidationError(
                status_code=404, error_code='TRANSFER00', error_message='Deck not found')

        file_name = f'deck_export_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}_{deck_id}.csv'
        url = url_for('static', filename=f'export/{file_name}', _external=True)
        exportDeck.delay(file_name, deck_id, current_user.id,
                         current_user.email, url)

        return jsonify(url=url)
