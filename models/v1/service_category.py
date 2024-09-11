#!/usr/bin/python3

from models.v1.base_model import BaseModel, Base
from sqlalchemy import Column, String

class ServiceCategory(BaseModel, Base):
    '''This defines the service categories table'''
    __tablename__ = 'service_categories'
    name = Column(String(128), nullable=False)
    image_url = Column(String(128), default='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)