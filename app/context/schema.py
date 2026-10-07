"""Pydantic models defining the V1 request and context JSON shape."""

from pydantic import BaseModel, ConfigDict, Field


class ContextRequest(BaseModel):
    """Data a client sends when asking the engine to build context."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    user_id: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    task: str = Field(min_length=1)


class UserProfile(BaseModel):
    """User profile data currently supplied by the V1 hardcoded collector."""

    id: str
    name: str
    education: str
    skills: list[str]
    projects: list[str]


class ContextResponse(BaseModel):
    """Complete context returned to the client."""

    user: UserProfile
    goal: str
    task: str
    memories: list[str]
    documents: list[str]
