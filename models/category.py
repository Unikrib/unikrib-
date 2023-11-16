#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column

class Category(BaseModel, Base):
    """This defines the service categories"""
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)