#!/usr/bin/python3

from datetime import datetime, timedelta
from models import storage


class Code():
    __tablename__ = 'codes'

    def __init__(self, *args, **kwargs):
        if "user_id" not in kwargs:
            raise ValueError("User id parameter is missing")
        if "code" not in kwargs:
            raise ValueError("Code parameter is missing")
        if "created_at" not in kwargs:
            setattr(self, "created_at", datetime.now())

        for key, val in kwargs.items():
            if key != '__class__':
                setattr(self, key, val)

    def save(self):
        """This save the code to storage"""
        storage.save(self)

    def get(self, user_id):
        if user_id is None:
            return None
        obj = storage.search('Code', user_id=user_id)
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
        obj = storage.search('Code', user_id=user_id)
        if obj is not None or len(obj) > 0:
            storage.delete(obj[0])
            storage.save()

    def to_dict(self):
        """This returns a dict representation of the object"""
        dictionary = self.__dict__.copy()
        if 'created_at' in dictionary and not isinstance(dictionary['created_at'], str):
            dictionary['created_at'] = self.created_at.isoformat()
        # dictionary.pop('_sa_instance_state', None)
        dictionary['__class__'] = self.__class__.__name__
        return dictionary