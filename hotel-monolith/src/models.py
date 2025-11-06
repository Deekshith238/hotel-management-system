from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float)
    available = db.Column(db.Boolean, default=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    name = db.Column(db.String)
    days = db.Column(db.Integer)
