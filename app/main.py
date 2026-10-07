"""FastAPI application entry point."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "Context Engine V1"))
app.include_router(router)
