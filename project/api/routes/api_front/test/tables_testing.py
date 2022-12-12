from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "client_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(10))
    client_channels: Mapped[list["ClientChannel"]] = relationship()

    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, chat_id={self.chat_id!r})"


class Channel(Base):
    __tablename__ = "channel_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    url_name: Mapped[str] = mapped_column(String(50))
    format: Mapped[int]
    last_id: Mapped[int | None]
    videos: Mapped[list["Video"]] = relationship()
    client_channels: Mapped[list["ClientChannel"]] = relationship()

    def __repr__(self) -> str:
        return f"Channel(id={self.id!r}, name={self.name!r})"


class ClientChannel(Base):
    __tablename__ = "clientchannel_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client_table.id"))
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel_table.id"))
    last_id: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f"ClientChannel(id={self.id!r}, client_id={self.client_id!r}, channel_id={self.channel_id!r}, last_id={self.client_id!r})"


class Video(Base):
    __tablename__ = "video_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(50))
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel_table.id"))

    def __repr__(self) -> str:
        return f"Video(id={self.id!r}, title={self.title!r}, channel_id={self.channel_id!r})"

    @staticmethod
    def from_array(array: list[list[str]], channel_id: int):
        return [
            Video(title=video[0], url=video[1], channel_id=channel_id)
            for video in array
        ]

    def __eq__(self, other) -> bool:
        return (
            (self.title == other.title)
            and (self.url == other.url)
            and (self.channel_id == other.channel_id)
        )
