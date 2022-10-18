from api.main import app
from fastapi import status
from fastapi.testclient import TestClient
from fixtures_test.conftest import expected_list_videos
from worker.utilities_worker import NoVideosFound

client = TestClient(app)


def test_request_videos_correct_result(mocker, expected_list_videos):
    object = mocker.MagicMock()
    object.get.return_value = expected_list_videos
    mocker.patch("api.main.get_videos.delay", return_value=object)
    response = client.get("/request_videos/channel")
    assert response.status_code == status.HTTP_200_OK
    list_videos = response.json()
    assert list_videos == expected_list_videos


def test_request_videos_raise_NoVideosFound_Exception(mocker):
    mocker.patch("api.main.get_videos.delay", side_effect=NoVideosFound())
    response = client.get("/request_videos/channel")
    assert response.status_code == status.HTTP_404_NOT_FOUND
