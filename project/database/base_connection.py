from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///videosDB.db", echo=True)

Session = sessionmaker(engine)


def create_metadata():
    Base.metadata.create_all(engine)


class Base(DeclarativeBase):
    pass
