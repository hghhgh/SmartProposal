from fastapi import APIRouter, Depends, Body
from app.core.vault_client import get_secret, set_secret
from app.core.security import require_roles

router = APIRouter()

admin_required = require_roles(["admin"])

@router.get("/get-key")
async def read_key(key_name: str, role: str = Depends(admin_required)):
    """
    دریافت کلید از Vault
    """
    return get_secret(key_name)

@router.post("/set-key")
async def store_key(
    key_name: str = Body(...),
    value: str = Body(...),
    role: str = Depends(admin_required)
):
    """
    ذخیره یا آپدیت کلید در Vault
    """
    return set_secret(key_name, value)
