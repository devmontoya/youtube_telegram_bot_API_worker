from api.schemas.requests import Filter, NewClient, NewClientChannelRequest
from api.url_parser.parser import extract_channel
from database.base_connection import Session
from database.db_service import ChannelDb, ClientChannelDb, ClientDb, VideoDb
from database.models.tables import Channel, Client, ClientChannel
from fastapi import APIRouter, HTTPException, status
from worker.utilities_worker import NoVideosFound
from worker.worker import get_videos

from .helper_functions import get_new_channels_videos_for_client

api_front = APIRouter(tags=["Front (Bot, Web)"])


@api_front.get("/get_client_id/{chat_id}", response_model=dict)
async def get_client_id(chat_id: str):
    with Session() as session:
        id_client = ClientDb.get_client_id_db(session, chat_id)
        if id_client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat_id no found"
            )
        return {"chat_id": chat_id, "client_id": id_client.id}


@api_front.get("/get_clients_channel_list/{client_id}", response_model=dict)
async def get_clients_channel_list(client_id: int):
    with Session() as session:
        client = ClientDb.get_element_by_id(session, client_id)
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="client id no found"
            )
        client_channel = client.channels
        channel_list = [channel_rela.channel for channel_rela in client_channel]
        channel_list = [
            {
                "channel_name": channel.name,
                "channel_url": f"www.youtube.com/c/{channel.url_name}",
            }
            for channel in channel_list
        ]
        return {"client_id": client_id, "channel_list": channel_list}


@api_front.post("/new_client_channel/")
async def new_client_channel(request: NewClientChannelRequest) -> dict:
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
            list_videos_from_selenium = request_videos(channel_name)
            new_channel = Channel(name=channel_name, url_name=channel_name, format=0)
            ChannelDb.add_new_element(session, new_channel)
            session.flush()
            channel_id = new_channel.id
            list_videos = VideoDb.add_new_channel_videos(
                session, list_videos_from_selenium, channel_id
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
            num_new_videos = len(list_videos)
        else:
            num_new_videos, list_videos = get_new_channels_videos_for_client(
                session, client, channel
            )
        result_list = [[video.title, video.url] for video in list_videos]
        session.commit()
    return {"num_new_videos": num_new_videos, "list_videos": result_list}


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


@api_front.post("/add_new_client/", response_model=dict)
def add_new_client(new_client_request: NewClient) -> dict:
    with Session() as session:
        new_client = Client(chat_id=new_client_request.chat_id)
        ClientDb.add_new_element(session, new_client)
        session.flush()
        client_id = new_client.id
        session.commit()
    return {"chat_id": new_client_request.chat_id, "client_id": client_id}


@api_front.get("/get_new_videos_for_client/{client_id}")
def get_new_videos_for_client(client_id: int):
    """Get all new videos from all channels for a client"""
    with Session() as session:
        client = ClientDb.get_element_by_id(session, client_id)
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="client no found"
            )

        client_channel = client.channels
        channels = [channel_rela.channel for channel_rela in client_channel]

        list_new_videos_channels = []
        for channel in channels:
            _, list_videos = get_new_channels_videos_for_client(
                session, client, channel
            )
            result_list = [[video.title, video.url] for video in list_videos]
            list_new_videos_channels.append(
                {"channel_name": channel.name, "list_new_videos": result_list}
            )
        session.commit()
    return list_new_videos_channels
