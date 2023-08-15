from datetime import datetime, timedelta
from uuid import uuid4

from sqlmodel import Field
from sqlmodel.ext.asyncio.session import AsyncSession

from .base import Base


class User(Base, table=True):  # type: ignore
    email: str = Field(nullable=False, unique=True)
    login_token: str | None = Field(nullable=True)
    token_expiration: datetime | None = Field(nullable=True)

    def token_is_valid(self):
        if not self.token_expiration:
            return False
        return self.token_expiration > datetime.now()

    async def update_login_token(self, session: AsyncSession):
        self.login_token = uuid4().hex
        self.token_expiration = datetime.now() + timedelta(minutes=15)
        await self.save(session)
        await session.commit()
        return self.login_token
