from fastapi import FastAPI
from app.middleware.ids_middleware import IDSMiddleware
from app.api.dashboard import router as dashboard_router
from app.api.dependency_api import router as dependency_router
from app.api.internal_test import router as internal_test_router

app = FastAPI(title="Security Dashboard")

app.add_middleware(IDSMiddleware)

app.include_router(dashboard_router, prefix="/dashboard")
app.include_router(dependency_router, prefix="/security")
app.include_router(internal_test_router, prefix="/security")
