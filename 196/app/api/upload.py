from fastapi import APIRouter, UploadFile, Depends
from app.core.security import require_roles

router = APIRouter()

@router.post("/")
async def upload_file(
    file: UploadFile,
    role: str = Depends(require_roles("writer", "admin"))
):
    content = await file.read()
    return {"filename": file.filename, "size": len(content), "role": role}
