from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"

def create_token(user_id: str, role: str):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, roles: list[str]):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload["role"] not in roles:
        raise Exception("Access denied")
    return payload
