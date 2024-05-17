from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Owner(db.Model):
    id = db.Column(db.String(150), primary_key=True)
    name = db.Column(db.String(150))
    age = db.Column(db.String(150))
    birth = db.Column(db.String(150))
    place_of_origin = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    email = db.Column(db.String(150))
    cars = db.relationship('Car')


class Car(db.Model):
    id = db.Column(db.String(150), primary_key=True)
    owner_id = db.Column(db.String(150), db.ForeignKey('owner.id'))
