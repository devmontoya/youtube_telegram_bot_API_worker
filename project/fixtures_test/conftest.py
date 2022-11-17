import pytest

expected_list_videos_array = [
    [
        "4 datos que marcan la histórica misión Artemis de la NASA para volver a la Luna",
        "/watch?v=bQzWu5-sQk8",
    ],
    [
        "A qué niveles llegan la pobreza, la desigualdad y la corrupción en Estados Unidos",
        "/watch?v=on_pdEdz7HA",
    ],
    [
        'Qué quieren decir los términos "ultraderecha" y "ultraizquierda" (y cómo se usan en la actualidad)',
        "/watch?v=Z0h4PCFvoo8",
    ],
    [
        "Quién es Ron DeSantis, el gran ganador republicano en Florida que supone un desafío para Trump",
        "/watch?v=DM-DEEa1SOs",
    ],
    [
        "Cómo llegó al poder el régimen que gobierna la República Islámica de Irán | BBC Mundo",
        "/watch?v=1wGiaxX2C-g",
    ],
]


@pytest.fixture
def expected_list_videos() -> list[list[str]]:
    return expected_list_videos_array
