import os
from models import *
import datetime


from flask import Flask, session, render_template, request, redirect, jsonify, url_for
from flask_session import Session
from sqlalchemy import create_engine, or_
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
        return render_template("login.html",name=session.get("email"))
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
                return redirect(url_for("home"))
            else:
                return render_template("registration.html", name = "Please enter correct password")
        else:
            return render_template("registration.html", name = "No user with this email")

@app.route("/logout",methods = ["GET"])
def logout():
    session.clear()
    return redirect("/register")
@app.route("/search", methods = ["POST","GET"])
def search():
    msg = ""
    book_obj=[]

    if request.method == "GET":
        if session.get("email") is not None:
            return render_template("login.html", book_obj=book_obj, msg=msg)
        else:
            return render_template("registration.html", name = "Please Login First")
    else:
        search_type = request.form.get("search_type")
        name = request.form.get("name")
        search = "%{}%".format(name)
        book_obj=[]

        if search_type == "title":
            book_obj = db.query(Book).filter(Book.title.like(search)).all()
            if len(book_obj) == 0:
                msg = "No results found"
            return render_template("login.html", book_obj=book_obj, msg=msg)
        elif search_type == "author":
            book_obj = db.query(Book).filter(Book.author.like(search)).all()
            if len(book_obj) == 0:
                msg = "No results found"
            return render_template("login.html", book_obj=book_obj, msg=msg)

        else:
            book_obj = db.query(Book).filter(Book.isbn.like(search)).all()
            if len(book_obj) == 0:
                msg = "No results found"
            return render_template("login.html", book_obj=book_obj, msg=msg)

# @app.route("/bookpage/<string:arg>",methods = ["GET"])
# def bookpage(arg):
#     if session.get("email") is not None:
#         isbn = arg.strip().split("=")[1]
#         book = db.query(Book).filter_by(isbn = isbn)
#         return render_template("bookpage.html", data = book)
#     else:
#         return redirect("/register")  

@app.route("/home")
def home():
    return render_template("home.html", username = session.get("email"))

@app.route("/bookpage/<string:arg>",methods = ["GET","POST"])
def bookpage(arg):
    if session.get("email") is None:
        return redirect("/register")
    print(arg)
    isbn = arg.strip().split("=")[1]

    book = SESSION.query(Book).filter_by(isbn = isbn).first()
    rating = SESSION.query(Review).filter_by(title=book.title).all()
    email = session.get("email")
    obj = SESSION.query(User).get(email)
    Uname = obj.name

    if request.method == "POST":
        # book = SESSION.query(Book).filter_by(isbn = isbn).first()
        title = book.title
        rating1 = request.form.get("rate")
        review = request.form.get("comment")
        temp = Review(Uname,title,rating1,review)
        # ratin = SESSION.query(Review).filter_by(title=book.title).all()

        try:
            SESSION.add(temp)
            SESSION.commit() 
            rating = SESSION.query(Review).filter_by(title=book.title).all()
            return render_template("review.html",data = book, name = Uname,rating = rating)
        except:
            SESSION.rollback()
            return render_template("review.html",data=book,text = "User already given review",rating = rating)
    else:
        return render_template("review.html",data = book, name = Uname ,rating = rating)

@app.route("/api/search", methods = ["POST", "GET"])
def api_search():
        data = request.form.get("key")
            # data = request.get_json()
        # key = data["key"]
        key = "%{}%".format(data)
        books = {"books":[]}
        filtered_list = db.query(Book).filter(or_(Book.isbn.like(key), Book.author.like(key), Book.title.like(key))).all()
        if filtered_list:
            if isinstance(filtered_list, list):
                for book in filtered_list:
                    d = dict()
                    d["isbn"] = book.isbn
                    d["title"] = book.title
                    d["author"] = book.author
                    books["books"].append(d)
                    print(book.isbn, book.title, book.author)
                return jsonify(books)
                    
            else :
                return jsonify({"isbn": filtered_list.isbn,"Title": filtered_list.title, "Author": filtered_list.author, "year": filtered_list.year})
        else:
            return jsonify({"error": "No books found"},400)

    # except:
        # return jsonify({"error": "Invalid request"},400)





  



          
