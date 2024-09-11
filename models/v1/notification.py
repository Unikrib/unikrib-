#!/usr/bin/python3

from models.v1.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, Boolean
# from sqlalchemy.orm import relationship


class Notification(BaseModel, Base):
    """This is the model for all notification instances"""
    __tablename__ = 'notifications'
    user_id = Column(String(60), nullable=False)
    text = Column(String(1024), nullable=False)
    last_opened = Column(DateTime, nullable=True)
    read = Column(Boolean, nullable=False, default=False)
    category = Column(String(60), nullable=False)
    item_id = Column(String(60), nullable=True)
    sender = Column(String(60), nullable=True)
    response = Column(String(60), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
