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
        # check if table exists
        if not cls.__table__.exists(bind=session.bind):
            cls.__table__.create(bind=session.bind)
        instance = cls.get(session, **kwargs)
        if instance:
            return instance
        return cls.create(session, **kwargs)