from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.security_events import log_event

class IDSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if response.status_code == 403:
            log_event(
                "UNAUTHORIZED_ACCESS",
                {
                    "path": request.url.path,
                    "method": request.method
                }
            )

        return response
