from api.main import app
from fastapi import status
from fastapi.testclient import TestClient
from fixtures_test.conftest import expected_list_videos

client = TestClient(app)


# def test_add_new_channel(mocker): # TODO
#     """Add a completely new channel"""
#     data = {"id_client": 1, "url_channel": "https://www.youtube.com/c/BBCMundo"}
#     response = client.post("/bot/add_channel", json=data)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == expected_list_videos
