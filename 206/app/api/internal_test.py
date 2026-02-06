from fastapi import APIRouter, Depends
from app.core.security import require_admin
from app.core.service_test import test_service_encryption

router = APIRouter()
CERT_PATH = "./certificates/server.crt"

@router.get("/test-communication")
async def test_internal_service(role_check=Depends(require_admin)):
    target_url = "https://localhost:8001/internal-data"
    result = test_service_encryption(target_url, CERT_PATH)
    return result
