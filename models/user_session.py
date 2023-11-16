#!/usr/bin/python3
"""This defines the schema for the user session storage
"""

from datetime import datetime
import models
from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime


class UserSession(Base):
    __tablename__ = 'usersession'
    token = Column(String(60), nullable=False, primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.now())

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def save(self):
        """This save the object to storage"""
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """This removes an object from storage"""
        models.storage.delete(self)
        models.storage.save()

    def to_dict(self):
        """This returns a dict representation of the object"""
        dictionary = self.__dict__.copy()
        if 'created_at' in dictionary:
            dictionary['created_at'] = self.created_at.isoformat()
        if 'updated_at' in dictionary:
            dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        dictionary['__class__'] = self.__class__.__name__
        return dictionary