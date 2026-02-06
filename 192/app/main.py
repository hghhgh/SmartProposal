from fastapi import FastAPI
from app.api.upload import router  # مسیر به فایل های api

app = FastAPI(title="SmartProposal Task 192")

app.include_router(router)
