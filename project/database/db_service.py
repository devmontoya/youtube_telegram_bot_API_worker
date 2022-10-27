from api.schemas.requests import Filter
from database.base_connection import Base
from database.models.tables import Channel, Client, ClientChannel, Video
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
    def get_all_elements_with_filter(cls, session, filter: Filter):
        stmt = select(cls.particular_model).where(
            getattr(cls.particular_model, filter.column) == filter.value
        )
        try:
            element = session.scalars(stmt).all()
            return element
        except NoResultFound:
            return None

    @classmethod
    def add_new_element(cls, session, new_element: Base) -> dict:
        session.add(new_element)
        return {"message": f"{new_element.__class__.__name__} added successfully"}

    @classmethod
    def get_element_by_id(cls, session, id: int):
        stmt = select(cls.particular_model).where(cls.particular_model.id == id)
        try:
            element = session.scalars(stmt).one()
            return element
        except NoResultFound:
            return None

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
        try:
            element = session.scalars(stmt).one()
            return element
        except NoResultFound:
            return None


class ClientDb(DbService):
    particular_model: Base = Client


class ChannelDb(DbService):
    particular_model: Base = Channel


class VideoDb(DbService):
    particular_model: Base = Video

    @classmethod
    def add_new_channel_videos(
        cls, session, list_videos: list[list[str]], channel_id: int
    ) -> list[Video]:
        """Adds new videos of a completely new channel"""
        video_objects = [
            Video(title=video[0], url=video[1], channel_id=channel_id)
            for video in list_videos
        ]
        video_objects = video_objects[::-1]  # Reversed order
        session.add_all(video_objects)
        return video_objects

    @classmethod
    def add_new_videos(
        cls, session, list_new_videos: list[list[str]], channel_id: int
    ) -> list[Video]:
        """Adds new videos, keeps only the 5 most recent ones"""
        list_new_videos = list_new_videos[::-1]  # Reversed order

        list_new_video_objects = Video.from_array(list_new_videos, 1)
        list_previous_videos = ChannelDb.get_element_by_id(session, channel_id).videos

        next_videos_to_add = []

        for video in list_new_video_objects:
            if not (video in list_previous_videos):
                next_videos_to_add.append(video)

        session.add_all(next_videos_to_add)
        session.flush()
        for video in list_previous_videos:
            if not (video in list_new_video_objects):
                session.delete(video)

        return list_new_video_objects


class ClientChannelDb(DbService):
    particular_model: Base = ClientChannel
