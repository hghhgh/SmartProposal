from fastapi import FastAPI
from app.middleware.ids_middleware import IDSMiddleware
from app.api.dashboard import router as dashboard_router
from app.api.dependency_api import router as dependency_router

app = FastAPI(title="Security Platform")

app.add_middleware(IDSMiddleware)

app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(dependency_router, prefix="/security")
