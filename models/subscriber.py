from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer

class Subscriber(BaseModel, Base):
    __tablename__ = 'subscribers'
    user_id = Column(ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)