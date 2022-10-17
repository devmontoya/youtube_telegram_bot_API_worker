from api.main import app
from fastapi import FastAPI
from fastapi.testclient import TestClient

expected_list_videos = [
    [
        "3 preguntas para entender la denuncia constitucional contra el presidente de Perú Pedro Castillo",
        "Los puntos calientes que dejó la desintegración de la Unión Soviética",
        "Las imágenes de la devastación tras el deslave en Venezuela #shorts",
        "Por qué los huracanes son tan frecuentes en México, Estados Unidos y el Caribe | BBC Mundo",
        "Los videos que muestran cómo se extendieron las protestas en Irán por la muerte de Mahsa Amini",
    ],
    [
        "/watch?v=ztNYKlx8jYg",
        "/watch?v=P_aTv7zLHBc",
        "/shorts/QAgsKZIm5ew",
        "/watch?v=YrK16AjSin0",
        "/watch?v=djwFy6ZS00k",
    ],
]


client = TestClient(app)


def test_get_videos_correct_result(mocker):
    object = mocker.MagicMock()
    object.get.return_value = expected_list_videos
    mocker.patch("api.main.get_videos.delay", return_value=object)
    response = client.get("/request_videos/channel")
    assert response.status_code == 200
    list_videos = response.json()
    assert list_videos == expected_list_videos
