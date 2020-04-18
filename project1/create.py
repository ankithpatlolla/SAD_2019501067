import os
from flask import Flask

from models import *

APP = Flask(__name__)

APP.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(APP)
def main():
    db.create_all()

if __name__ == '__main__':
    with APP.app_context():
        main()
