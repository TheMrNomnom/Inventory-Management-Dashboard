from . import db
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, hash):
        self.username = username
        self.hash = hash

    def __repr__(self):
        return f"<User {self.username}>"


class Item(db.Model, SerializerMixin):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)

    def __init__(self, item_name, quantity, location_id):
        self.item_name = item_name
        self.quantity = quantity
        self.location_id = location_id

    def __repr__(self):
        return f"<Item {self.item_name}>"


class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name
