# database.py
#
# This file sets up the database connection using SQLAlchemy for the Math Microservice.
# It configures:
#   - the SQLite database engine (`test.db`)
#   - a session factory to interact with the database (`SessionLocal`)
#   - a declarative base class for defining ORM models (`Base`)
#
# It also provides a `get_db()` dependency function used with FastAPI's Depends()
# to manage opening and closing database sessions in a clean and reusable way.


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()