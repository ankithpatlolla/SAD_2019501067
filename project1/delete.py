import os
from models import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
ENGINE = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=ENGINE))
session = db()

User.__table__.drop(ENGINE)
print("table deleted")
