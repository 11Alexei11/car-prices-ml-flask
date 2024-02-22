from flask import Flask

import sys
import os
sys.path.append(os.getcwd())

from users.views import users_bp
from src.app import db
from src.app.users.models.initialize_db import create_tables


create_tables(db)


app = Flask(__name__)
app.register_blueprint(users_bp)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


app.run(host='0.0.0.0', port=8080, debug=True)
