import os
from models import *
import datetime

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
SESSION = db()

@app.route("/")
def index():
    if session.get("email") is not None:
        return render_template("login.html")
    else:
        return redirect("/register")

@app.route("/register",methods = ["GET", "POST"])
def signup():
    if session.get("email") is not None:
        return render_template("login.html")
    else:    
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            print("name : ", name)
            print("email : ", email)
            timestamp = datetime.datetime.now()
            # print("timestamp ::", timestamp)
            user = User(name=name,email=email,password=password,timestamp=timestamp)
            # print("user added")
            try:
                SESSION.add(user)
                # print("add done")
                SESSION.commit()
                # print("commit done")
                return render_template("registration.html", name = "Hi, your registration is successful")
            except:
                return render_template("registration.html", name = "User is already exist")
        else:
            return render_template("registration.html")

@app.route("/admin",methods = ["GET"])
def tabledetails():
    data = db.query(User)
    return render_template("admin.html",data = data)

@app.route("/auth", methods = ["POST"])
def authorized():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        thisuser = db.query(User).get(email)
        if thisuser != None:
            if password == thisuser.password:
                session["email"] = email
                return render_template("login.html", name = name)
            else:
                return render_template("registration.html", name = "Please enter correct password")
        else:
            return render_template("registration.html", name = "No user with this email")

@app.route("/logout",methods = ["GET"])
def logout():
    session.clear()
    return redirect("/register")
          
