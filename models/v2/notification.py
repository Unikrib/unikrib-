#!/usr/bin/python3

from models.base_model import BaseModel


class Notification(BaseModel):
    __tablename__ = 'notifications'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {"user_id": "User id", "text": "Text",
                           "category": "Category"}
        for key, value in required_params.items():
            if key not in kwargs:
                raise ValueError(f"{value} parameter is missing")
            
        if "read" not in kwargs:
            setattr(self, 'read', False)

        # other optional parameters:
        # sender: str
        # last_opened: Datetime
        # item_id: str
        # response: str