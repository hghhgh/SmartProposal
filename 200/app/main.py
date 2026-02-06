# app/main.py
from fastapi import FastAPI
from app.api import security_scan

app = FastAPI()

app.include_router(security_scan.router)
