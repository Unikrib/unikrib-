#!/usr/bin/python3

from models.v2.base_model import BaseModel


class Category(BaseModel):
    __tablename__ = 'categories'

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        if "name" not in kwargs:
            raise ValueError("Name parameter is missing")