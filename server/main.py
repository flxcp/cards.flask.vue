from api.cardAPI import CardAPI
from api.deckAPI import DeckAPI
from api.deckTransferAPI import DeckExport, DeckImport, DeckBatchExport, DeckBatchImport
from api.reviewAPI import ReviewAPI
from api.userAPI import UserAPI, UpdateEmailAPI, UpdatePasswordAPI, GetAllDecks
from api.registerAPI import RegisterAPI
from api.testAPI import TestAPI
from app.jobs import workers
from flask import Flask
from flask_restful import Api
from app.security import user_datastore, sec
from app.db import db
from app.cache import cache
import logging
import app.config as config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config)

# Enable Flask Cache
cache.init_app(app)
CORS(app)

# Flask Database Settings
db.init_app(app)

# Enable Celery
celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
)
celery.Task = workers.ContextTask


@app.before_first_request
def create_db():
    db.create_all()


# Flask Logging
logging.basicConfig(filename='cards.log', level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(name)s in %(module)s: %(message)s')

# Flask API
api = Api(app)
api.init_app(app)

# Flask Security
sec.init_app(app, user_datastore)

# Declare Context
app.app_context().push()


# Add all RESTful controllers
api.add_resource(TestAPI, "/api/test/")
api.add_resource(UserAPI, "/api/user/")
api.add_resource(GetAllDecks, "/api/decks/")
api.add_resource(UpdateEmailAPI, "/api/email/")
api.add_resource(RegisterAPI, "/api/register/")
api.add_resource(UpdatePasswordAPI, "/api/password/")
api.add_resource(DeckExport, "/api/deckexport/<int:deck_id>/")
api.add_resource(DeckBatchExport, "/api/deckbatchexport/<int:deck_id>/")
api.add_resource(DeckImport, "/api/deckimport/<int:deck_id>/")
api.add_resource(DeckBatchImport, "/api/deckbatchimport/<int:deck_id>/")
api.add_resource(DeckAPI, "/api/deck/", "/api/deck/<int:deck_id>/")
api.add_resource(CardAPI, "/api/card/", "/api/card/<int:card_id>/")
api.add_resource(ReviewAPI, "/api/card/<int:card_id>/res/<int:response>/")

if __name__ == '__main__':
    app.run()
