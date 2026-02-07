"""
Middleware امنیتی برای FastAPI
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import SecurityMiddleware as SecurityMiddlewareService


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware برای افزودن هدرهای امنیتی به پاسخ‌ها"""
    
    def __init__(self, app, security_service: SecurityMiddlewareService):
        super().__init__(app)
        self.security_service = security_service
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # افزودن هدرهای امنیتی
        security_headers = self.security_service.get_security_headers()
        for header, value in security_headers.items():
            response.headers[header] = value
        
        return response




