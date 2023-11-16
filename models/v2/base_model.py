#!/usr/bin/python3

from models import storage
from datetime import datetime
import uuid

time3 = "%Y-%m-%dT%H:%M:%S"
time2 = "%Y-%m-%dT%H:%M:%S.%f"
time = "%d-%m-%Y %H:%M"

class BaseModel():
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    def __init__(self, *args, **kwargs):
        """class initialization"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                try:
                    self.created_at = datetime.strptime(kwargs["created_at"], time)
                except Exception as e:
                    try:
                        self.created_at = datetime.strptime(kwargs["created_at"], time2)
                    except Exception as e:
                        try:
                            self.created_at = datetime.strptime(kwargs["created_at"], time3)
                        except Exception as e:
                            print("Error at base_model:", e)
            else:
                self.created_at = datetime.utcnow()
                self.created_at = self.created_at.strftime("%d-%m-%Y %H:%M")
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                try:
                    self.updated_at = datetime.strptime(kwargs["updated_at"], time)
                except Exception as e:
                    try:
                        self.updated_at = datetime.strptime(kwargs["updated_at"], time2)
                    except Exception as e:
                        try:
                            self.updated_at = datetime.strptime(kwargs["updated_at"], time3)
                        except Exception as e:
                            print(e)
            else:
                self.updated_at = datetime.utcnow()
                self.updated_at = self.updated_at.strftime("%d-%m-%Y %H:%M")
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def to_dict(self):
        """This returns a dict representation of the object"""
        dictionary = self.__dict__.copy()
        if 'created_at' in dictionary and isinstance(dictionary['created_at'], datetime):
            dictionary['created_at'] = self.created_at.isoformat()
        if 'updated_at' in dictionary and isinstance(dictionary['updated_at'], datetime):
            dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        dictionary.pop('reset_code', None)
        dictionary['__class__'] = self.__class__.__name__
        return dictionary
    
    def __str__(self):
        """Called when print function is used"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.to_dict())

    def save(self):
        """This save the object to storage"""
        self.updated_at = datetime.utcnow()
        self.updated_at = self.updated_at.strftime("%d-%m-%Y %H:%M")
        storage.save(self)

    def update(self, **kwargs):
        """This updates some attribute in storage"""
        try:
            for key, val in kwargs.items():
                if key == "password":
                    if self.reset_code == "Valid":
                        setattr(self, key, val)
                    else:
                        pass
                else:
                    setattr(self, key, val)
                storage.save(self)
        except Exception:
            pass

    def delete(self):
        """This removes an object from storage"""
        storage.delete(self)
