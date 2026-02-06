from fastapi import Header, HTTPException, Depends

def require_roles(required_roles: list):
    async def role_checker(x_role: str = Header(...)):
        if x_role.lower() not in [role.lower() for role in required_roles]:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")
        return x_role
    return role_checker
