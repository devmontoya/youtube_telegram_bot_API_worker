import pytest

expected_list_videos_array = [
    [
        "3 preguntas para entender la denuncia constitucional contra el presidente de Perú Pedro Castillo",
        "/watch?v=ztNYKlx8jYg",
    ],
    [
        "Los puntos calientes que dejó la desintegración de la Unión Soviética",
        "/watch?v=P_aTv7zLHBc",
    ],
    [
        "Las imágenes de la devastación tras el deslave en Venezuela #shorts",
        "/shorts/QAgsKZIm5ew",
    ],
    [
        "Por qué los huracanes son tan frecuentes en México, Estados Unidos y el Caribe | BBC Mundo",
        "/watch?v=YrK16AjSin0",
    ],
    [
        "Los videos que muestran cómo se extendieron las protestas en Irán por la muerte de Mahsa Amini",
        "/watch?v=djwFy6ZS00k",
    ],
]


@pytest.fixture
def expected_list_videos() -> list[list[str]]:
    return expected_list_videos_array
