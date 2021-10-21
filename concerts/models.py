from datetime import datetime
from flask_login import UserMixin

from . import db


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    artist = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    venue = db.Column(db.String(255))
    status = db.Column(db.String(255))
    desc = db.Column(db.Text)
    tickets = db.Column(db.Integer)
    price = db.Column(db.Float)
    image = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    comments = db.relationship("Comment", backref="event")
    bookings = db.relationship("Booking", backref="event")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    desc = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    tickets = db.Column(db.Integer)
    price = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, nullable=False, unique=True)
    hash = db.Column(db.String(255), nullable=False)

    comments = db.relationship("Comment", backref="user")
    bookings = db.relationship("Booking", backref="user")
