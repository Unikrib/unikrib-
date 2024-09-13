#!/usr/bin/python3

from models.v2.base_model import BaseModel


class School(BaseModel):
    __tablename__ = 'schools'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {'name': 'Name', 'full_name': 'Full_name',
                           'city': 'City', 'image_url': 'Image_url'}
        
        for key, value in required_params.items():
            if key not in kwargs:
                raise ValueError(f'{value} field is missing')
