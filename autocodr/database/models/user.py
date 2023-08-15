from datetime import datetime

from sqlmodel import Field

from .base import Base


class User(Base, table=True):  # type: ignore
    email: str = Field(nullable=False, unique=True)
    login_token: str | None = Field(nullable=True)
    token_expiration: datetime | None = Field(nullable=True)

    def token_is_valid(self):
        if not self.token_expiration:
            return False
        return self.token_expiration > datetime.now()
