import re


def extract_channel(text: str) -> list[str, int]:
    patterns = [
        r"(?:https:\/\/)?www\.youtube\.com(?:\/c)?\/(\w*)(?:(?:\/featured)|(?:\/videos))?",
        r"(?:https:\/\/)?www\.youtube\.com(?:\/channel)?\/([\w-]*)(?:(?:\/featured)|(?:\/videos))?",
    ]
    return [re.findall(patterns[0], text)[0], 0]
