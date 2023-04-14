from .engine import session_maker
from sqlalchemy import select


async def get(cls, **kwargs):
    """ Returns an instance of the class if it exists, otherwise returns None. """
    async with session_maker() as session:
        return (await session.execute(select(cls).filter_by(**kwargs))).scalar_one_or_none()


async def create(cls, **kwargs):
    """ Creates an instance of the class and adds it to the database. """
    async with session_maker() as session:
        instance = cls(**kwargs)
        session.add(instance)
        await session.commit()
        return instance


async def get_or_create(cls, **kwargs):
    """ Returns an instance of the class if it exists, otherwise creates it. """
    instance = await get(cls, **kwargs)
    if instance:
        return instance
    return await create(cls, **kwargs)