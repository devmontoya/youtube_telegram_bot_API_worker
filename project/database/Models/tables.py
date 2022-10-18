from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from base_connection import Base


class Client(Base):
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(10))


class Channel(Base):
    __tablename__ = "channel"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    url_name: Mapped[str] = mapped_column(String(30))
    format: Mapped[int]
    videos: Mapped[list["Video"]] = relationship()


class Video(Base):
    __tablename__ = "video"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(30))
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"))
