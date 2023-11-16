#!/usr/bin/python3

from models.base_model import BaseModel


class Service(BaseModel):
    __tablename__ = 'services'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {"category_id": "Category id", "owner_id": "Owner id",
                           "description": "Description"}
        for key, val in required_params.items():
            if key not in kwargs:
                raise ValueError(f"{val} parameter is missing")
            
        default_params = {"image1": "images/white_image.jpg", "image2": "images/white_image.jpg",
                          "image3": "images/white_image.jpg", "image4": "images/white_image.jpg",
                          "image5": "images/white_image.jpg"}
        for key, val in default_params.items():
            if key not in kwargs:
                setattr(self, key, val)