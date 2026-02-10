from fastapi import FastAPI
from app.api.upload import router

app = FastAPI()
app.include_router(router)
