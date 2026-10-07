"""FastAPI application entry point."""

import os
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.api.routes import router
from app.database.connection import Base, engine
from app.database import models as _models  # Register ORM models with Base.metadata.


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Create the V2 tables when the application starts."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=os.getenv("APP_NAME", "Context Engine V2"),
    lifespan=lifespan,
)
app.include_router(router)
