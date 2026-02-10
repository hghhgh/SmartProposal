# app/api/version_api.py

from fastapi import APIRouter
from app.core.version_check import check_versions_auto

router = APIRouter()

# می‌توانی نسخه‌های مورد نیاز پروژه خودت رو اینجا مشخص کنی
REQUIRED_VERSIONS = {
    "fastapi": "0.100.0",
    "uvicorn": "0.23.2"
}

@router.get("/versions")
def version_check():
    """
    بررسی نسخه پکیج‌ها و نشان دادن ناسازگاری یا قدیمی بودن.
    """
    issues = check_versions_auto(REQUIRED_VERSIONS)
    return {"versions": issues}
