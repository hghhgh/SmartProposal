from fastapi import APIRouter, UploadFile, Depends
from app.core.security import require_roles

router = APIRouter()


@router.post("/up")
def upload_file(file: UploadFile, role: str = Depends(require_roles("admin", "writer"))):
    return {"message": "File uploaded successfully", "role": role}

