# app/main.py

from fastapi import FastAPI
from app.api.version_api import router as version_router

app = FastAPI(title="Version Checker API")

app.include_router(version_router, prefix="/api")
