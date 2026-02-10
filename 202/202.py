from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
import logging
import os
import json
from datetime import datetime

# ------------------ تنظیم لاگ JSON ------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "access.json")

logger = logging.getLogger("access_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter("%(message)s"))  # JSON مستقیم
logger.addHandler(file_handler)

# ------------------ اپ و امنیت ------------------
app = FastAPI()
security = HTTPBearer()

# شبیه‌سازی پایگاه داده کاربران و نقش‌ها
USERS = {
    "admin_token": {"username": "admin", "role": "admin"},
    "user_token": {"username": "user1", "role": "user"}
}


# ------------------ کمک‌کننده‌ها ------------------
def get_client_ip(request: Request):
    return request.client.host


def log_access(client_ip, user, method, path, role, status):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "client_ip": client_ip,
        "user": user,
        "role": role,
        "method": method,
        "path": path,
        "status": status
    }
    logger.info(json.dumps(log_entry))


# ------------------ دکوریتور برای endpoint حساس ------------------
def sensitive_endpoint(roles_allowed=None):
    roles_allowed = roles_allowed or ["admin"]  # پیش‌فرض فقط admin

    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security), *args,
                          **kwargs):
            token = credentials.credentials
            user_info = USERS.get(token)
            if not user_info:
                log_access(get_client_ip(request), "unknown", request.method, request.url.path, "unknown",
                           "unauthorized")
                raise HTTPException(status_code=403, detail="Unauthorized")

            if user_info["role"] not in roles_allowed:
                log_access(get_client_ip(request), user_info["username"], request.method, request.url.path,
                           user_info["role"], "forbidden")
                raise HTTPException(status_code=403, detail="Forbidden")

            log_access(get_client_ip(request), user_info["username"], request.method, request.url.path,
                       user_info["role"], "success")
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator


# ------------------ Endpointهای نمونه ------------------
@app.get("/sensitive-data")
@sensitive_endpoint(roles_allowed=["admin"])
async def sensitive_data(request: Request):
    return {"message": "This is sensitive data for admins"}


@app.get("/moderator-data")
@sensitive_endpoint(roles_allowed=["admin", "moderator"])
async def moderator_data(request: Request):
    return {"message": "Data for admin and moderators"}


@app.get("/public-data")
async def public_data():
    return {"message": "This is public data, no log needed"}
