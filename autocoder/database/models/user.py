from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from ..base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    login_token = Column(String, nullable=True)
    token_expiration = Column(DateTime, nullable=True)
    
    def token_is_valid(self):
        return self.token_expiration > datetime.now()
