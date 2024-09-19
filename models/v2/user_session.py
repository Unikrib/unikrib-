#!/usr/bin/python3

from datetime import datetime
from models import storage
from models.v2.base_model import BaseModel


class UserSession(BaseModel):
    __tablename__ = 'usersession'

    def __init__(self, *args, **kwargs):
        if "token" not in kwargs:
            raise ValueError("Token parameter missing")
        if "user_id" not in kwargs:
            raise ValueError("User id parameter missing")
        
        super().__init__(*args, **kwargs)
        # if "created_at" not in kwargs:
        #     self.created_at = datetime.now()

        for key, val in kwargs.items():
            if key != '__class__':
                setattr(self, key, val)

    # def save(self):
    #     """This save the object to storage"""
    #     storage.save(self)

    # def delete(self):
    #     """This removes an object from storage"""
    #     storage.delete(self)
    #     storage.save(self)

    # def to_dict(self):
    #     """This returns a dict representation of the object"""
    #     dictionary = self.__dict__.copy()
    #     if 'created_at' in dictionary and not isinstance(dictionary['created_at'], str):
    #         dictionary['created_at'] = self.created_at.isoformat()
    #     if 'updated_at' in dictionary:
    #         dictionary['updated_at'] = self.updated_at.isoformat()
    #     dictionary.pop('_sa_instance_state', None)
    #     dictionary['__class__'] = self.__class__.__name__
    #     return dictionary