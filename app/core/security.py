"""
ماژول امنیتی سیستم
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import secrets
import hashlib
from pathlib import Path
import json


class SecuritySettings:
    """مدیریت تنظیمات امنیتی سیستم"""
    
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self._ensure_config_file()
    
    def _ensure_config_file(self):
        """ایجاد فایل تنظیمات در صورت عدم وجود"""
        if not self.config_file.exists():
            default_config = {
                "encryption_enabled": True,
                "https_required": True,
                "max_file_size_mb": 50,
                "allowed_file_types": [".odt"],
                "rate_limiting": {
                    "enabled": True,
                    "requests_per_minute": 60
                },
                "authentication": {
                    "enabled": False,
                    "session_timeout_minutes": 30
                },
                "cors": {
                    "allowed_origins": ["http://localhost:3000"],
                    "allow_credentials": True
                },
                "headers": {
                    "x_content_type_options": "nosniff",
                    "x_frame_options": "DENY",
                    "x_xss_protection": "1; mode=block",
                    "strict_transport_security": "max-age=31536000; includeSubDomains"
                }
            }
            self.config_file.write_text(
                json.dumps(default_config, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
    
    def get_config(self) -> Dict[str, Any]:
        """دریافت تنظیمات"""
        try:
            content = self.config_file.read_text(encoding="utf-8")
            return json.loads(content) if content else {}
        except:
            return {}
    
    def update_config(self, **kwargs):
        """به‌روزرسانی تنظیمات"""
        config = self.get_config()
        config.update(kwargs)
        config["last_updated"] = datetime.now().isoformat()
        self.config_file.write_text(
            json.dumps(config, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )


class EncryptionService:
    """سرویس رمزنگاری ارتباطات"""
    
    @staticmethod
    def generate_secret_key() -> str:
        """تولید کلید مخفی"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """هش کردن رمز عبور"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # استفاده از SHA-256 برای هش
        hash_obj = hashlib.sha256()
        hash_obj.update((password + salt).encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        
        return password_hash, salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """بررسی صحت رمز عبور"""
        computed_hash, _ = EncryptionService.hash_password(password, salt)
        return computed_hash == password_hash


class SecurityMiddleware:
    """Middleware امنیتی برای افزودن هدرهای امنیتی"""
    
    def __init__(self, security_config: SecuritySettings):
        self.security_config = security_config
    
    def get_security_headers(self) -> Dict[str, str]:
        """دریافت هدرهای امنیتی"""
        config = self.security_config.get_config()
        headers_config = config.get("headers", {})
        
        headers = {}
        if "x_content_type_options" in headers_config:
            headers["X-Content-Type-Options"] = headers_config["x_content_type_options"]
        if "x_frame_options" in headers_config:
            headers["X-Frame-Options"] = headers_config["x_frame_options"]
        if "x_xss_protection" in headers_config:
            headers["X-XSS-Protection"] = headers_config["x_xss_protection"]
        if "strict_transport_security" in headers_config:
            headers["Strict-Transport-Security"] = headers_config["strict_transport_security"]
        
        return headers




