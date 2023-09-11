# models.py

from sqlalchemy import Column, Integer, String, Float
from database import Base

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True,autoincrement=False, index=True, nullable=False)
    location_name = Column(String(100), index=True)
    latitude = Column(Float)
    longitude = Column(Float)

