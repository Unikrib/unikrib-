#!/usr/bin/python3

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Transaction(BaseModel, Base):
    """Contains references of all the transactions made"""
    __tablename__ = 'transactions'
    userId = Column(ForeignKey('users.id'))  # Payer of the money
    itemId = Column(String(60), nullable=False)
    reference = Column(String(60), nullable=False)
    status = Column(String(60), default="failed")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)