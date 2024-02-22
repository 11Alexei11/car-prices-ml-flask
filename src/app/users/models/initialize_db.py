from peewee import Database

from src.app.users.models.user import User


def create_tables(db: Database):
    """Function to perform creation of tables in db

    Args:
        db (Database): Source database
    """
    with db:
        db.create_tables([User])