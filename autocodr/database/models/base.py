from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import Self


class Base(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    @classmethod
    async def get(cls, session: AsyncSession, **kwargs) -> Self | None:
        try:
            return (await session.execute(select(cls).filter_by(**kwargs))).scalar_one_or_none()
        except:
            await session.rollback()
            return None

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> Self:
        try:
            return await cls(**kwargs).save(session)
        except:
            await session.rollback()
            raise

    @classmethod
    async def from_id(cls, session: AsyncSession, id: UUID) -> Self | None:
        try:
            return await cls.get(session, id=id)
        except:
            await session.rollback()
            return None

    @classmethod
    async def get_or_create(cls, session: AsyncSession, **kwargs) -> Self:
        try:
            return (await cls.get(session, **kwargs)) or (await cls.create(session, **kwargs))
        except:
            await session.rollback()
            raise

    async def save(self, session: AsyncSession) -> Self:
        try:
            session.add(self)
            await session.commit()
            await session.refresh(self)
            return self
        except:
            await session.rollback()
            raise

    async def delete(self, session: AsyncSession) -> None:
        try:
            await session.delete(self)
            await session.commit()
        except:
            await session.rollback()
            raise

    async def update(self, session: AsyncSession, **data) -> Self:
        try:
            for key, value in data.items():
                setattr(self, key, value)
            return await self.save(session)
        except:
            await session.rollback()
            raise

    async def refresh(self, session: AsyncSession) -> Self:
        try:
            await session.refresh(self)
            return self
        except:
            await session.rollback()
            raise
