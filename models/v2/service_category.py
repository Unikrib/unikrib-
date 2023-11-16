#!/usr/bin/python3

from models.base_model import BaseModel


class ServiceCategory(BaseModel):
    __tablename__ = 'service_categories'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "name" not in kwargs:
            raise ValueError("Name parameter is missing")