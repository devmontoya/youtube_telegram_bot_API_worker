import re

from api.schemas.requests import channel_from_url


def extract_channel(text: str) -> channel_from_url:
    """Extracts the name of a channel from a youtube url"""
    patterns = [
        r"(?:https:\/\/)?www\.youtube\.com(?:\/c)?\/(\w*)(?:(?:\/featured)|(?:\/videos))?",
        r"(?:https:\/\/)?www\.youtube\.com(?:\/channel)?\/([\w-]*)(?:(?:\/featured)|(?:\/videos))?",
    ]
    return channel_from_url(name=re.findall(patterns[0], text)[0], format=0)
