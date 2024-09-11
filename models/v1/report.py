#!/usr/bin/python3

from models.v1.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

class Report(BaseModel, Base):
    __tablename__ = 'reports'
    topic = Column(String(255), nullable=False)
    description = Column(String(1024, collation='utf8mb4_unicode_ci'), nullable=True)
    reporter = Column(String(60), ForeignKey('users.id'), nullable=True)
    reported = Column(String(60), ForeignKey('users.id'), nullable=False)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)