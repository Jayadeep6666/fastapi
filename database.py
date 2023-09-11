# database.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session
DATABASE_URL = "sqlite:///./addresses.db"
Base = declarative_base()

# Create the "addresses" table if it doesn't exist
# Base.metadata.create_all(bind=engine)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
