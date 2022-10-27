from api.schemas.requests import Filter, NewClientChannelRequest
from api.url_parser.parser import extract_channel
from database.base_connection import Session
from database.db_service import ChannelDb, ClientDb, VideoDb
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
        else:
            list_videos = ChannelDb.get_element_with_filter(
                session, Filter(column="name", value=channel_name)
            ).videos
        result_list = [[video.title, video.url] for video in list_videos]
        session.commit()
    return result_list


@api_front.get("/request_videos/{channel}", response_model=list[list[str]])
def request_videos(channel: str) -> list[list[str]]:
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
