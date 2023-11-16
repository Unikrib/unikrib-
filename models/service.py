#!/usr/bin/python3\
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Service(BaseModel, Base):
    """This defines the services class"""
    __tablename__ = 'services'
    
    category_id = Column(String(60), ForeignKey('service_categories.id'), nullable=False)
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    description = Column(String(1024, collation='utf8mb4_unicode_ci'), nullable=False)
    image1 = Column(String(128), nullable=True, default='images/white_image.jpg')
    image2 = Column(String(128), nullable=True, default='images/white_image.jpg')
    image3 = Column(String(128), nullable=True, default='images/white_image.jpg')
    image4 = Column(String(128), nullable=True, default='images/white_image.jpg')
    image5 = Column(String(128), nullable=True, default='images/white_image.jpg')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)