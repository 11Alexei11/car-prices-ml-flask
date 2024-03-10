from peewee import TextField, FloatField, AutoField, ForeignKeyField, IntegerField

from src.utils.base_model import BaseModel
from src.app.users.models.user import User


class Prediction(BaseModel):
    """Class implements logic of peewee table"""

    calculation_id = AutoField()
    user_id = ForeignKeyField(model=User, field=User.user_id, backref="CarParams")

    symboling = TextField(null=False)
    car_name = TextField(null=False)
    fuel_type = TextField(null=False)
    aspiration = TextField(null=False)
    door_number = TextField(null=False)
    car_body = TextField(null=False)
    drive_wheel = TextField(null=False)
    engine_location = TextField(null=False)
    wheel_base = FloatField(null=False)
    car_length = FloatField(null=False)
    car_width = FloatField(null=False)
    car_height = FloatField(null=False)
    curb_weight = FloatField(null=False)
    engine_type = TextField(null=False)
    cylinder_number = TextField(null=False)
    engine_size = IntegerField(null=False)
    fuel_system = TextField(null=False)
    bore_ratio = FloatField(null=False)
    stroke = FloatField(null=False)
    compression_ratio = FloatField(null=False)
    horse_power = IntegerField(null=False)
    peak_rpm = IntegerField(null=False)
    city_mpg = IntegerField(null=False)
    highway_mpg = TextField(null=False)

    price = FloatField(null=False)
