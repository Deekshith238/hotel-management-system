from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rooms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String)
    price = db.Column(db.Float)
    available = db.Column(db.Boolean, default=True)

with app.app_context():
    db.create_all()
    if not Room.query.first():
        db.session.add_all([
            Room(room_type="Single", price=1500, available=True),
            Room(room_type="Double", price=2500, available=True),
            Room(room_type="Suite", price=4000, available=True)
        ])
        db.session.commit()

@app.route('/rooms')
def get_rooms():
    rooms = Room.query.filter_by(available=True).all()
    return jsonify([{"id": r.id, "room_type": r.room_type, "price": r.price} for r in rooms])

if __name__ == "__main__":
    app.run(port=5001, debug=True)
