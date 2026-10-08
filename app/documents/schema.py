"""API models for adding and listing documents."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=100_000)


class DocumentResponse(BaseModel):
    id: int
    title: str
    chunk_count: int
    created_at: datetime
