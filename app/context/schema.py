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

class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    education: str = Field(min_length=1, max_length=300)
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)


class UserUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=200)
    education: str | None = Field(default=None, min_length=1, max_length=300)
    skills: list[str] | None = None
    projects: list[str] | None = None

class ContextResponse(BaseModel):
    """Complete context returned to the client."""

    user: UserProfile
    goal: str
    task: str
    memories: list[str]
    documents: list[str]
