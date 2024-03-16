#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float, Boolean, Integer, Text
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This defines the user class"""
    __tablename__ = 'users'
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    password = Column(String(60), nullable=False)
    phone_no = Column(Integer, nullable=True)
    user_type = Column(String(60), nullable=False)
    com_res = Column(String(60), nullable=True)
    avatar = Column(String(256), nullable=True, default='https://res.cloudinary.com/deg1j9wbh/image/upload/v1710551753/default-img_rthe0v.webp')
    note = Column(String(length=256, collation='utf8mb4_unicode_ci'), nullable=True, default='I provide the best products/services')
    rating = Column(Float, nullable=False, default=0)
    isVerified = Column(Boolean, nullable=False, default=False)
    reset_code = Column(String(60), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
