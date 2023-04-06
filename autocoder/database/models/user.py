from sqlalchemy import Column, Integer, String
from ..base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    
    def __init__(self, name, email=None):
        self.name = name
        self.email = email
     
