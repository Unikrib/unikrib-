#!/usr/bin/python3

from models.v2.base_model import BaseModel

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
            self.avatar = "https://res.cloudinary.com/deg1j9wbh/image/upload/v1710551753/default-img_rthe0v.webp"
        if "rating" not in kwargs:
            self.rating = 0
        if "isVerified" not in kwargs:
            self.isVerified = False
        if 'verification_status' not in kwargs:
            self.verification_status = 'unverified'
        if kwargs['user_type'] not in ['regular', 'agent', 'vendor', 'sp']:
            raise ValueError("Invalid user type passed.")
