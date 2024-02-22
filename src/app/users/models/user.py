from peewee import Model, TextField, BooleanField, AutoField

from src.app import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = AutoField()
    name = TextField(null=False)
    email = TextField(null=False)
    password = TextField(null=False)
    is_admin = BooleanField(default=False)
