# app/api/security_scan.py
from fastapi import APIRouter, HTTPException
from app.core.dependency_scan import check_vulnerabilities

router = APIRouter()

@router.get("/security/dependency-scan")
def dependency_scan():
    try:
        vulnerabilities = check_vulnerabilities()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    if vulnerabilities:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Vulnerable dependencies detected",
                "count": len(vulnerabilities),
                "vulnerabilities": vulnerabilities,
                "action": "Update or patch affected packages"
            }
        )

    return {"status": "clean"}
