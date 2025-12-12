from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class user_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(100))
    avg_screentime = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, age, gender, avg_screentime, created_at):
        self.age = age
        self.gender = gender
        self.avg_screentime = avg_screentime
        self.created_at = created_at


# Serve the new frontend
@app.route("/")
def home():
    return render_template("screentime-enhanced.html")


# NEW: API endpoint to save data
@app.route("/save-data", methods=["POST"])
def save_data():
    try:
        data = request.json
        hours = float(data['hours'])
        minutes = float(data['minutes'])
        age = int(data['age'])
        gender = data['gender']
        avg_screentime = hours + minutes / 60
        created_at = datetime.now()

        # Add user to database
        new_user = user_data(
            age=age,
            gender=gender,
            avg_screentime=avg_screentime,
            created_at=created_at
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Keep this commented unless you need to create DB again
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)