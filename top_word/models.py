from typing import Any

from pydantic import BaseModel, Field


# main models
class WordOfTheDay(BaseModel):
    word: str
    timestamp: str


class TopicOfTheDay(BaseModel):
    header: str = Field(max_length=50)
    body: str = Field(max_length=300)


# exception handlers models
class DetailMessage(BaseModel):
    errors: Any  # json errors, primarily validation errors
    body: Any = None
    status_code: int
    error_codes: list[str] | None = None


class ErrorResponse(BaseModel):
    detail: DetailMessage
