#!/usr/bin/python3

from models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {"text": "Text", "reviewer": "Reviewer",
                           "reviewee": "Reviewee", "star": "Star"}
        for key, val in required_params.items():
            if key not in kwargs:
                raise ValueError(f"{val} parameter is missing")