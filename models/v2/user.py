#!/usr/bin/python3

from models.base_model import BaseModel

class User(BaseModel):
    """This defines the user class"""
    __tablename__ = 'users'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {"first_name": "First name", "email": "Email",
                           "password": "Password", "phone_no": "Phone number",
                           "user_type": "User type"}
        
        for key, val in required_params.items():
            if key not in kwargs:
                raise ValueError(f"{val} is missing")
            
        # set default values for some fields
        if "note" not in kwargs:
            self.note = "I provide the best products/services"
        if "avatar" not in kwargs:
            self.avatar = "images/default-img.webp"
        if "rating" not in kwargs:
            self.rating = 0
        if "isVerified" not in kwargs:
            self.isVerified = False
        if kwargs['user_type'] not in ['regular', 'agent', 'vendor', 'sp']:
            raise ValueError("Invalid user type passed.")
