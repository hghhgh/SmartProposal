from fastapi import Header, HTTPException, status, Depends


def get_current_role(x_role: str = Header(...)):
    return x_role


def require_roles(*allowed_roles):
    def role_checker(role: str = Depends(get_current_role)):
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: role mismatch"
            )
        return role
    return role_checker


