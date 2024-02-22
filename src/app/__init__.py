from peewee import PostgresqlDatabase


db = PostgresqlDatabase("car_price.db")
db.init('car_price.db')

