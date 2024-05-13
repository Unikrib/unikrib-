#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

class School(BaseModel, Base):
    __tablename__ = 'schools'
    name = Column(String(124), nullable=False)
    full_name = Column(String(1024), nullable=False)
    city = Column(String(124), nullable=False)
    image_url = Column(String(126), nullable=False)
