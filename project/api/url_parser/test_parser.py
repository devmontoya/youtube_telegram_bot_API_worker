import pytest

from .parser import extract_channel


@pytest.mark.parametrize("y", ["/videos", "/featured", "/"])
@pytest.mark.parametrize("x", ["/c/", "/"])
def test_parse_url_format_0(mocker, x, y):
    """Check the most basic url pattern"""
    format_test = "https://www.youtube.com" + x + "BBCMundo" + y
    result = extract_channel(format_test)
    assert result[0] == "BBCMundo"
    assert result[1] == 0
