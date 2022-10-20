from pydantic import BaseModel, Field


class NewClientChannelRequest(BaseModel):
    chat_id: str
    url: str = Field(..., max_length=60)


class Filter(BaseModel):
    column: str
    value: int | str
