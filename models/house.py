#!/usr/bin/python3
"""This defines the apartment class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class House(BaseModel, Base):
    """Class definition"""
    __tablename__ = 'houses'
    price = Column(Integer, nullable=False)
    agent_fee = Column(Integer, nullable=True)
    apartment = Column(String(128), nullable=False)
    name = Column(String(128), nullable=True)
    street_id = Column(ForeignKey('streets.id'))
    running_water = Column(String(3), nullable=True)
    waste_disposal = Column(String(3), nullable=True)
    image1 = Column(String(128), nullable=True, default="https://res.cloudinary.com/deg1j9wbh/image/upload/v1710551500/white_image_vasgxl.jpg")
    image2 = Column(String(128), nullable=True, default="https://res.cloudinary.com/deg1j9wbh/image/upload/v1710551500/white_image_vasgxl.jpg")
    image3 = Column(String(128), nullable=True, default="https://res.cloudinary.com/deg1j9wbh/image/upload/v1710551500/white_image_vasgxl.jpg")
    owner_id = Column(ForeignKey('users.id'), nullable=False)
    features = Column(String(length=5000, collation='utf8mb4_unicode_ci'), nullable=True, default="")
    newly_built = Column(Boolean, default=False)
    tiled = Column(Boolean, default=False)
    rooms_available = Column(Integer, default=1)
    security_available = Column(Boolean, default=False)
    daily_power = Column(Integer, default=12)
    no_clicks = Column(Integer, default=0)
    balcony = Column(Boolean, default=True)
    furnished = Column(Boolean, default=False)
    env_id = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
