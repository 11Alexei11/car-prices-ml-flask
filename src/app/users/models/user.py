from uuid import uuid4

from peewee import TextField, BooleanField, UUIDField

from src.utils.base_model import BaseModel


class User(BaseModel):
    user_id = UUIDField(unique=True, null=False, primary_key=True, default=uuid4)
    name = TextField(null=False)
    email = TextField(null=False)
    password = TextField(null=False)
    is_admin = BooleanField(default=False)
