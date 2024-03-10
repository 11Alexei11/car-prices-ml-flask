from peewee import Model

from src.app import db


class BaseModel(Model):
    class Meta:
        database = db