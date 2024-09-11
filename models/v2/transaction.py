#!/usr/bin/python3

from models.v2.base_model import BaseModel


class Transaction(BaseModel):
    __tablename__ = 'transactions'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {"user_id": "User id", "reference": "Reference",
                           "item_id": "Item id"}
        for key, val in required_params.items():
            if key not in kwargs:
                raise ValueError(f"{val} parameter is missing")
            
        if "status" not in kwargs:
            setattr(self, "status", "failed")