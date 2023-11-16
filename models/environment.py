#!/usr/bin/python3
"""This defines the environment e.g Ekosodin, Bdpa ..."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Environment(BaseModel, Base):
    """Class definition"""
    __tablename__ = 'environments'
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
