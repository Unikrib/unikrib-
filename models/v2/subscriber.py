#!/usr/bin/python3

from models.v2.base_model import BaseModel


class Subscriber(BaseModel):
    __tablename__ = 'subscribers'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {'user_id': 'User_id'}

        for key, value in required_params.items():
            if key not in kwargs:
                raise ValueError(f'{value} field is missing')