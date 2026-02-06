from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI(title="SmartProposal with IDS")

app.include_router(upload_router, prefix="/upload", tags=["Upload"])
