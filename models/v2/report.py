#!/usr/bin/python3

from models.v2.base_model import BaseModel


class Report(BaseModel):
    __tablename__ = 'reports'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "topic" not in kwargs:
            raise ValueError("Topic parameter missing")
        if "reported" not in kwargs:
            raise ValueError("Reported parameter is missing")
        
        # other parameters include:
        # reporter: str
        # description: str