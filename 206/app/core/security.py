from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    if token != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return token
