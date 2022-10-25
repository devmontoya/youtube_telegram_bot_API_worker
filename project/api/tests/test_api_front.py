import pytest
from api.main import app
from api.tests.tables_testing import Video
from fastapi import status
from fastapi.testclient import TestClient
from fixtures_test.conftest import expected_list_videos
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

client = TestClient(app)


def test_request_videos_correct_result(mocker, expected_list_videos):
    object = mocker.MagicMock()
    object.get.return_value = expected_list_videos
    mocker.patch("api.routes.api_front.base.get_videos.delay", return_value=object)
    response = client.get("/api_front/request_videos/channel")
    assert response.status_code == status.HTTP_200_OK
    list_videos = response.json()
    assert list_videos == expected_list_videos


def test_update_video_five_existing_videos_add_one(mocker, session_fixture):
    prepare_five_videos(session_fixture)
    new_video = [["video_6", "url_6"]]
    mocker.patch(
        "api.routes.api_front.base.ChannelDb.get_element_by_id", return_value=1
    )
    object = mocker.MagicMock()
    object.return_value.get.return_value = new_video
    mocker.patch("api.routes.api_front.base.get_videos.delay", return_value=object)
    Session = mocker.MagicMock()
    Session.return_value.__enter__.return_value = session_fixture
    Session.return_value.__exit__.return_value = True
    mocker.patch("api.routes.api_front.base.Session", return_value=Session())
    response = client.get("/api_front/update_videos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == new_video


def test_tests_db(mocker, session_fixture):
    Session = mocker.MagicMock()
    Session.return_value.__enter__.return_value = session_fixture
    Session.return_value.__exit__.return_value = True
    mocker.patch("api.routes.api_front.base.Session", return_value=Session())
    response = client.get("/api_front/tests_db/5687")
    assert response.status_code == status.HTTP_200_OK


@pytest.fixture()
def session_fixture(mocker):
    from .tables_testing import Base

    engine = create_engine("sqlite:///test_DB.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine, autocommit=False, autoflush=False)
    session = Session()
    yield session
    session.rollback()


def prepare_five_videos(session):
    videos = [
        Video(title=f"video_{i}", url=f"url_{i}", channel_id=1) for i in range(1, 6)
    ]
    session.add_all(videos)
