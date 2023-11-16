#!/usr/bin/python3

from models.base_model import BaseModel


class Environment(BaseModel):
    __tablename__ = 'environments'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "name" not in kwargs:
            raise ValueError("Name parameter is missing")