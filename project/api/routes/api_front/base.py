from api.schemas.requests import NewClientChannelRequest
from database.base_connection import Session
from database.db_service import ClientDb
from database.models.tables import Client
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


@api_front.post("/new_client_channel/")
async def new_client_channel(request: NewClientChannelRequest):
    with Session() as session:
        id_client = ClientDb.get_client_id_db(session, request.chat_id)
        if id_client is None:
            new_client = Client(chat_id=request.chat_id)
            ClientDb.add_new_element(session, new_client)
        session.commit()
    return True


@api_front.get("/request_videos/{channel}", response_model=list[list[str]])
def request_videos(channel: str):
    try:
        task = get_videos.delay(channel)
        videos = task.get()
    except NoVideosFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return videos
