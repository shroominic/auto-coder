from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .base import Base

DATABASE_URL = getenv("DATABASE_URL") or "sqlite:///autocoder/database/db.sqlite3"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

def init_db():
    Base.metadata.create_all(bind=engine)
