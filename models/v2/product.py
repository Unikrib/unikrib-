#!/usr/bin/python3

from models.v2.base_model import BaseModel
# from models import BaseModel


class Product(BaseModel):
    __tablename__ = 'products'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_params = {"name": "Name", "price": "Price",
                           "owner_id": "Owner id", "category_id": "Category id"}
        for key, val in required_params.items():
            if key not in kwargs:
                raise ValueError(f"{val} parameter is missing")
            
        default_params = {"delivery": "no", "image1": "images/white_image.jpg",
                          "image2": "images/white_image.jpg",
                          "image3": "images/white_image.jpg", "available": "yes"}
        for key, val in default_params.items():
            if key not in kwargs:
                setattr(self, key, val)

        if not isinstance(self.price, int):
            try:
                if isinstance(self.price, str):
                    setattr(self, 'price', int(self.price))
            except Exception as e:
                raise TypeError("Price value must be a number")