from flask import Flask, render_template, request, redirect, url_for
from models import db, Room, Booking

# ✅ Tell Flask where to find the templates folder (outside src)
app = Flask(__name__, template_folder='../templates')

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables and sample data
with app.app_context():
    db.create_all()
    if not Room.query.first():
        db.session.add_all([
            Room(room_type="Single", price=1500, available=True),
            Room(room_type="Double", price=2500, available=True),
            Room(room_type="Suite", price=4000, available=True)
        ])
        db.session.commit()

# Routes
@app.route('/')
def home():
    rooms = Room.query.filter_by(available=True).all()
    return render_template('index.html', rooms=rooms)

@app.route('/book/<int:room_id>', methods=['GET','POST'])
def book(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        name = request.form['name']
        days = int(request.form['days'])
        booking = Booking(room_id=room.id, name=name, days=days)
        room.available = False
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('booking.html', room=room)

# Run the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
