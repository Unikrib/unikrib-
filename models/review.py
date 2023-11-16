#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer

class Review(BaseModel, Base):
    """This defines the reviews class"""
    __tablename__ = 'reviews'
    text = Column(String(2048, collation='utf8mb4_unicode_ci'), nullable=False)
    reviewer = Column(ForeignKey('users.id'), nullable=False)
    reviewee = Column(ForeignKey('users.id'), nullable=False)
    star = Column(String(2), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
