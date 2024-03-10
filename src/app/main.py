from logging.config import dictConfig
import secrets
import json
import sys
import os
sys.path.append(os.getcwd())

from flask import Flask

from src.app.users.views import users_bp
from src.app.price_predictions.views import car_price_blue_print
from src.app import db
from src.utils.db_utils import create_tables
from src.utils.config import ConfigLoader


create_tables(db)

config = ConfigLoader.load()
print(json.dumps(config, indent=4))

dictConfig(config=config["logging.config"])


app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(car_price_blue_print)
app.secret_key = secrets.token_hex(32)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


app.run(host='0.0.0.0', port=8080, debug=True)
