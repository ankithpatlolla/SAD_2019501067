from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


    def _init_(self,name,email,password,timestamp):
        self.name = name
        self.email = email
        self.password = password
        self.timestamp = timestamp
