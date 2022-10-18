import pytest
from fixtures_test.conftest import expected_list_videos
from worker.worker import get_videos


def test_get_videos(mocker, expected_list_videos):
    f = open("worker/tests/bbcmundo.html", "rb")
    html = f.read()
    mocker.patch("worker.worker.CustomDriver", return_value=True)
    mocker.patch("worker.worker.fetch_html", return_value=html)
    f.close()
    list_videos = get_videos("bbcmundo")
    assert list_videos == expected_list_videos
