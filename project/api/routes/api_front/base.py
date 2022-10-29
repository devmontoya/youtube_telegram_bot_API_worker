from api.schemas.requests import Filter, NewClientChannelRequest
from api.url_parser.parser import extract_channel
from database.base_connection import Session
from database.db_service import ChannelDb, ClientChannelDb, ClientDb, VideoDb
from database.models.tables import Channel, Client, ClientChannel, Video
from fastapi import APIRouter, HTTPException, status
from worker.utilities_worker import NoVideosFound
from worker.worker import get_videos

api_front = APIRouter(tags=["Front (Bot, Web)"])


@api_front.get("/get_client_id/{chat_id}")
async def get_client_id(chat_id: str):
    with Session() as session:
        id_client = ClientDb.get_client_id_db(session, chat_id)
        if id_client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat_id no found"
            )
        return id_client.id


@api_front.post("/new_client_channel/", response_model=list[list[str]])
async def new_client_channel(request: NewClientChannelRequest) -> list[list[str]]:
    """Endpoint for a potencial new channel and client"""
    with Session() as session:
        client = ClientDb.get_element_by_id(session, request.client_id)
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Client id no found"
            )

        channel_name = extract_channel(request.url).name
        # Try to find out if this channel already exists in the DB
        channel = ChannelDb.get_element_with_filter(
            session, Filter(column="name", value=channel_name)
        )
        if channel is None:
            list_videos_list = request_videos(channel_name)
            new_channel = Channel(name=channel_name, url_name=channel_name, format=0)
            ChannelDb.add_new_element(session, new_channel)
            session.flush()
            channel_id = new_channel.id
            list_videos = VideoDb.add_new_channel_videos(
                session, list_videos_list, channel_id
            )
            # Update the last video id in channel table
            session.flush()
            print(list_videos[-1].id)
            last_id_video = list_videos[-1].id
            new_channel.last_id = last_id_video
            new_client_channel = ClientChannel(
                client_id=client.id, channel_id=channel_id, last_id=last_id_video
            )
            ClientChannelDb.add_new_element(session, new_client_channel)
            session.flush()
        else:
            channel_id = channel.id
            list_videos = ChannelDb.get_element_with_filter(
                session, Filter(column="name", value=channel_name)
            ).videos
            last_id_video = list_videos[-1].id
            client_channel_relationship = (
                ClientChannelDb.get_element_with_double_filter(
                    session,
                    Filter(column="client_id", value=client.id),
                    Filter(column="channel_id", value=channel_id),
                )
            )
            if client_channel_relationship is None:
                new_client_channel = ClientChannel(
                    client_id=client.id, channel_id=channel_id, last_id=last_id_video
                )
                ClientChannelDb.add_new_element(session, new_client_channel)
            else:
                """Compares the last video with the last one known for the user"""
                num_new_videos = client_channel_relationship.last_id - channel.last_id
                if num_new_videos < 0:
                    list_videos = list_videos[num_new_videos:]
        result_list = [[video.title, video.url] for video in list_videos]
        session.commit()
    return result_list


@api_front.get("/request_videos/{channel}", response_model=list[list[str]])
def request_videos(channel: str) -> list[list[str]]:
    """Request a list of videos from a youtube channel via Selenium worker"""
    try:
        task = get_videos.delay(channel)
        videos = task.get()
    except NoVideosFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return videos


@api_front.get("/update_videos/{channel_id}", response_model=list[list[str]])
def update_videos(channel_id: int) -> list[list[str]]:
    try:
        with Session() as session:
            channel_name = ChannelDb.get_element_by_id(session, channel_id).name
            task = get_videos.delay(channel_name)
            videos = task.get()
            print(videos)
            VideoDb.add_new_videos(session, videos, channel_id)
            session.commit()
    except NoVideosFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return videos


@api_front.get("/add_new_client/{chat_id}", response_model=int)
def add_new_client(chat_id: str) -> int:
    with Session() as session:
        new_client = Client(chat_id=chat_id)
        ClientDb.add_new_element(session, new_client)
        session.flush()
        client_id = new_client.id
        session.commit()
    return client_id
