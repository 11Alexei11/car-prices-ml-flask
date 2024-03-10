from peewee import Database

from src.utils.base_model import db
from src.app.users.models.user import User
from src.app.price_predictions.models.prediction import Prediction


def create_tables(db: Database):
    """Function to perform creation of tables in db

    Args:
        db (Database): Source database
    """
    with db:
        db.create_tables([User, Prediction])


