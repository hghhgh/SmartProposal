from fastapi import APIRouter, Depends, HTTPException
from app.core.security import require_admin
from app.core.dependency_scan import run_dependency_scan

router = APIRouter()

@router.get("/dependency-scan")
def dependency_scan(role=Depends(require_admin)):
    result = run_dependency_scan()

    if result["status"] == "vulnerable":
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Vulnerable dependencies detected",
                "vulnerabilities": result["details"]
            }
        )

    return {"status": "clean"}
