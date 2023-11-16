#!/usr/bin/python3
"""This defines the schema for the user session storage
"""

from datetime import datetime, timedelta
import models
from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime

class Code(Base):
    __tablename__ = 'codes'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False, primary_key=True)
    code = Column(String(60), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def save(self):
        """This save the code to storage"""
        models.storage.new(self)
        models.storage.save()

    def get(self, user_id):
        if user_id is None:
            return None
        obj = models.storage.search('Code', user_id=user_id)
        if obj is None or len(obj) == 0:
            return None
        user = obj[0]
        ttl = 30 * 1000
        valid_period = user.created_at + timedelta(seconds = ttl)
        if valid_period < datetime.now():
            self.delete_code(user.user_id)
            return None
        return user.code

    def delete_code(self, user_id):
        """This removes the code from storage"""
        obj = models.storage.search('Code', user_id=user_id)
        if obj is not None or len(obj) > 0:
            models.storage.delete(obj[0])
            models.storage.save()

    def to_dict(self):
        """This returns a dict representation of the object"""
        dictionary = self.__dict__.copy()
        if 'created_at' in dictionary:
            dictionary['created_at'] = self.created_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        dictionary['__class__'] = self.__class__.__name__
        return dictionary