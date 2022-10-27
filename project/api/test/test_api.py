from api.main import app
from fastapi import status
from fastapi.testclient import TestClient
from fixtures_test.conftest import expected_list_videos

client = TestClient(app)
