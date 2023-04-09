from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class SpecialBase(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def get(cls, session, **kwargs):
        return session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def create(cls, session, **kwargs):
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def get_or_create(cls, session, **kwargs):
        instance = cls.get(session, **kwargs)
        if instance:
            return instance
        return cls.create(session, **kwargs)