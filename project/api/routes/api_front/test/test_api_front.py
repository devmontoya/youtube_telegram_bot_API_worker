import pytest
from api.main import app
from api.routes.api_front.test.tables_testing import Channel, Video
from database.db_service import ChannelDb, VideoDb
from fastapi import status
from fastapi.testclient import TestClient
from fixtures_test.conftest import expected_list_videos
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from worker.utilities_worker import NoVideosFound

client = TestClient(app)


def test_request_videos_correct_result(mocker, expected_list_videos):
    get_videos = mocker.patch("api.routes.api_front.base.get_videos")
    task = get_videos.delay()
    task.get.return_value = expected_list_videos
    response = client.get("/api_front/request_videos/channel")
    assert response.status_code == status.HTTP_200_OK
    list_videos = response.json()
    assert list_videos == expected_list_videos


def test_request_videos_raise_NoVideosFound_Exception(mocker):
    mocker.patch(
        "api.routes.api_front.base.get_videos.delay", side_effect=NoVideosFound()
    )
    response = client.get("/api_front/request_videos/channel")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_video_five_existing_videos_add_one(mocker, session_fixture):
    previous_videos = prepare_five_videos(session_fixture)
    new_videos = previous_videos[1:] + [["video_6", "url_6"]]

    ChannelDb.add_new_element(
        session_fixture, Channel(name="channel_1", url_name="channel_1", format=0)
    )

    channel_object = mocker.patch("api.routes.api_front.base.ChannelDb")()
    channel_object.get_element_by_id.return_value = "channel_1"

    task = mocker.MagicMock()
    task.get.return_value = new_videos
    mocker.patch("api.routes.api_front.base.get_videos.delay", return_value=task)

    Session = mocker.patch("api.routes.api_front.base.Session")
    Session.return_value = session_fixture

    response = client.get("api_front/update_videos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == new_videos
    assert VideoDb.get_all_elements(session_fixture) == Video.from_array(
        new_videos, channel_id=1
    )


@pytest.fixture()
def session_fixture():
    from .tables_testing import Base

    engine = create_engine(
        "sqlite://",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return Session(engine)


def prepare_five_videos(session):
    videos = [[f"video_{i}", f"url_{i}"] for i in range(1, 6)]
    video_objects = [
        Video(title=video[0], url=video[1], channel_id=1) for video in videos
    ]
    session.add_all(video_objects)
    session.flush()
    return videos
