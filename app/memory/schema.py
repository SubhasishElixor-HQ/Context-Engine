"""Pydantic models for the V3 memory API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MemoryExtractRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    conversation_text: str = Field(min_length=1, max_length=10_000)


class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    content: str
    category: str
    created_at: datetime


class MemoryExtractionResponse(BaseModel):
    extracted_count: int
    memories: list[MemoryResponse]