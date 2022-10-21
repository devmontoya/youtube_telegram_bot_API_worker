from pydantic import BaseModel, Field


class NewClientChannelRequest(BaseModel):
    client_id: int = Field(default=1)
    url: str = Field(default="www.youtube.com/c/bbcmundo", max_length=60)


class channel_from_url(BaseModel):
    name: str
    format: int


class Filter(BaseModel):
    column: str
    value: int | str
