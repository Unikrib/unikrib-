#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

class ServiceCategory(BaseModel, Base):
    '''This defines the service categories table'''
    __tablename__ = 'service_categories'
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)