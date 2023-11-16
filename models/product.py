#!/usr/bin/python3
"""defines the various services rendered by the service providers"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """This defines the service objects"""
    __tablename__ = 'products'
    name = Column(String(128), nullable=False)
    price = Column(Integer, nullable=False)
    delivery = Column(String(5), nullable=False, default='no')
    features = Column(String(length=2048, collation='utf8mb4_unicode_ci'), nullable=True)
    image1 = Column(String(128), nullable=True, default='images/white_image.jpg')
    image2 = Column(String(128), nullable=True, default='images/white_image.jpg')
    image3 = Column(String(128), nullable=True, default='images/white_image.jpg')
    available = Column(String(5), nullable=False, default='yes')
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


