#!/usr/bin/python3
"""Defines the streets"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Street(BaseModel, Base):
    """class definition"""
    __tablename__ = 'streets'
    name = Column(String(128), nullable=False)
    env_id = Column(ForeignKey('environments.id'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
