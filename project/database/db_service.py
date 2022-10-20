from api.schemas.requests import Filter
from database.base_connection import Base
from database.models.tables import Client
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


class DbService:

    particular_model: Base

    @classmethod
    def get_all_elements(cls, session):
        statement = select(cls.particular_model)
        elements = session.scalars(statement).all()
        return elements

    @classmethod
    def add_new_element(cls, session, new_element: Base) -> dict:
        session.add(new_element)
        return {"message": f"{new_element.__class__.__name__} added successfully"}

    @classmethod
    def get_element_by_id(cls, session, id: int):
        stmt = select(cls.particular_model).where(cls.particular_model.id == id)
        element = session.scalars(stmt).one()
        return element

    @classmethod
    def get_client_id_db(cls, session, chat_id: str):
        stmt = select(cls.particular_model).where(
            cls.particular_model.chat_id == chat_id
        )
        try:
            element = session.scalars(stmt).one()
            return element
        except NoResultFound:
            return None

    @classmethod
    def get_element_with_filter(cls, session, filter: Filter):
        stmt = select(cls.particular_model).where(
            getattr(cls.particular_model, filter.column) == filter.value
        )
        element = session.scalars(stmt).one()
        return element


class ClientDb(DbService):
    particular_model: Base = Client
