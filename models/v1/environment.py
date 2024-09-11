#!/usr/bin/python3
"""This defines the environment e.g Ekosodin, Bdpa ..."""

from models.v1.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Environment(BaseModel, Base):
    """Class definition"""
    __tablename__ = 'environments'
    name = Column(String(128), nullable=False)
    school_id = Column(ForeignKey('schools.id'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
