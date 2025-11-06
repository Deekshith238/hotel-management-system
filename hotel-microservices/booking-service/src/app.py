from flask import Flask, render_template, request, redirect, url_for
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer)
    name = db.Column(db.String)
    days = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    rooms = requests.get('http://127.0.0.1:5001/rooms').json()
    return render_template('index.html', rooms=rooms)

@app.route('/book/<int:room_id>', methods=['GET','POST'])
def book(room_id):
    if request.method == 'POST':
        name = request.form['name']
        days = int(request.form['days'])
        booking = Booking(room_id=room_id, name=name, days=days)
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('booking.html', room_id=room_id)

if __name__ == "__main__":
    app.run(port=5002, debug=True)
