from fastapi import APIRouter, UploadFile, Depends
from app.security.crypto import encrypt_file
from app.storage.temp_storage import save_temp_file
from app.security.audit import log
from app.core.config import ENCRYPTION_KEY
import uuid

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile):
    raw = await file.read()
    encrypted = encrypt_file(raw, ENCRYPTION_KEY)
    file_id = str(uuid.uuid4())
    save_temp_file(file_id, encrypted)
    log("user", f"upload {file.filename}")
    return {"file_id": file_id}
