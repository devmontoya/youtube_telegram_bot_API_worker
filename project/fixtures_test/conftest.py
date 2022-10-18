import pytest

expected_list_videos_array = [
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


@pytest.fixture
def expected_list_videos():
    return expected_list_videos_array
