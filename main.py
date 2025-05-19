from flask import Flask, render_template, url_for, redirect, request, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from calculation import yearly_screen_time, life_expectancy, lifetime_screentime
from dotenv import load_dotenv
import os



app = Flask(__name__)
load_dotenv()
app.secret_key= os.getenv("SECRET_KEY")

##Creating database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#This is temporary to create the DB(once)
with app.app_context():
    db.create_all()


class user_data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(100))
    avg_screentime = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)

    def __init__(self, age, gender, avg_screentime, created_at):
        self.age = age
        self.gender = gender
        self.avg_screentime = avg_screentime
        self.created_at = created_at
        


@app.route("/", methods=["POST","GET"])
def home():
    results = None
    if request.method =="POST":
        hours = float(request.form["hours"])
        minutes = float(request.form["minutes"])
        age = int(request.form["age"])
        gender = request.form["gender"]
        avg_screentime = hours + minutes/60 # converting time into a decimal
        created_at= datetime.now()

        #Adding user to the database
        new_user = user_data(
            age = age, gender = gender, 
            avg_screentime = avg_screentime, created_at= created_at
            )
        db.session.add(new_user)
        db.session.commit()

        #Calculations
        yearly = yearly_screen_time(avg_screentime)
        life_exp = life_expectancy(gender, age)
        lifetime = lifetime_screentime(avg_screentime, life_exp)

        # Creating a dictionary with the data and results
        session["results"]={
            "hours": int(hours),
            "minutes": int(minutes),
            "screentime": avg_screentime,
            "gender": gender,
            "age": age,
            "yearly_summary":{
                "months": yearly[0],
                "days": yearly[1]
                },
            "life_expectancy": life_exp,
            "lifetime_use": {
                "years": lifetime[0],
                "months": lifetime[1],
                }
        }
        return redirect(url_for("home"))

    results = session.pop("results", None)
    return render_template("index_wmobile.html", results = results)



if __name__ == "__main__":
    app.run()

