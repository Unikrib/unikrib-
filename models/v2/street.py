#!/usr/bin/python3

from models.v2.base_model import BaseModel


class Street(BaseModel):
    __tablename__ = 'streets'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {"name": "Name", "env_id": "Environmental id"}
        for key, val in required_params.items():
            if key not in kwargs:
                raise ValueError(f"{val} parameter is missing")
            