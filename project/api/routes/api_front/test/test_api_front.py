import pytest
from api.main import app
from api.routes.api_front.base import api_front
from api.routes.api_front.test.tables_testing import Video
from fastapi import status
from fastapi.testclient import TestClient
from fixtures_test.conftest import expected_list_videos
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
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
    new_video = previous_videos[1:] + ["video_6", "url_6"]
    channel_object = mocker.MagicMock()
    channel_object.get.return_value = new_video
    mocker.patch(
        "api.routes.api_front.base.ChannelDb.get_element_by_id",
        return_value=channel_object,
    )
    object = mocker.MagicMock()
    object.get.return_value = new_video
    mocker.patch("api.routes.api_front.base.get_videos.delay", return_value=object)
    Session = mocker.MagicMock()
    Session.return_value.__enter__.return_value = session_fixture
    Session.return_value.__exit__.return_value = True
    mocker.patch("api.routes.api_front.base.Session", return_value=Session())
    response = client.get("api_front/update_videos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == new_video


# def test_tests_db(mocker, session_fixture):
#     Session = mocker.MagicMock()
#     Session.return_value.__enter__.return_value = session_fixture
#     Session.return_value.__exit__.return_value = True
#     Session = mocker.patch("api.routes.api_front.base.Session")
#     Session.return_value.__enter__.return_value = session_fixture
#     response = client.get("api_front/tests_db/5687")
#     assert response.status_code == status.HTTP_200_OK


@pytest.fixture()
def session_fixture(mocker):
    from .tables_testing import Base

    engine = create_engine("sqlite:///test_DB.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()
    yield session
    session.close()


def prepare_five_videos(session):
    videos = [[f"video_{i}", f"url_{i}"] for i in range(1, 6)]
    video_objects = [
        Video(title=video[0], url=video[1], channel_id=1) for video in videos
    ]
    session.add_all(video_objects)
    session.flush()
    return videos
