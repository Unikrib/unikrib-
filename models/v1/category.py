#!/usr/bin/python3

from models.v1.base_model import BaseModel, Base
from sqlalchemy import String, Column

class Category(BaseModel, Base):
    """This defines the service categories"""
    __tablename__ = 'categories'
    name = Column(String(128), nullable=False)
    image_url = Column(String(128), nullable=False, default='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)