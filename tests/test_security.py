"""
تست‌های امنیت و مجوزها
"""

import unittest
from pathlib import Path
from app.core.security import SecuritySettings, EncryptionService


class TestSecuritySettings(unittest.TestCase):
    """تست تنظیمات امنیتی"""
    
    def setUp(self):
        """تنظیمات اولیه"""
        self.config_file = Path("test_security_config.json")
        if self.config_file.exists():
            self.config_file.unlink()
        self.security_settings = SecuritySettings(self.config_file)
    
    def tearDown(self):
        """پاکسازی بعد از تست"""
        if self.config_file.exists():
            self.config_file.unlink()
    
    def test_default_config(self):
        """تست تنظیمات پیش‌فرض"""
        config = self.security_settings.get_config()
        self.assertIn("encryption_enabled", config)
        self.assertIn("https_required", config)
        self.assertIn("rate_limiting", config)
    
    def test_update_config(self):
        """تست به‌روزرسانی تنظیمات"""
        self.security_settings.update_config(encryption_enabled=False)
        config = self.security_settings.get_config()
        self.assertFalse(config["encryption_enabled"])


class TestEncryptionService(unittest.TestCase):
    """تست سرویس رمزنگاری"""
    
    def test_generate_secret_key(self):
        """تست تولید کلید مخفی"""
        key = EncryptionService.generate_secret_key()
        self.assertIsInstance(key, str)
        self.assertGreater(len(key), 20)
    
    def test_hash_password(self):
        """تست هش کردن رمز عبور"""
        password = "test_password_123"
        password_hash, salt = EncryptionService.hash_password(password)
        
        self.assertIsInstance(password_hash, str)
        self.assertIsInstance(salt, str)
        self.assertGreater(len(password_hash), 0)
        self.assertGreater(len(salt), 0)
    
    def test_verify_password(self):
        """تست بررسی صحت رمز عبور"""
        password = "test_password_123"
        password_hash, salt = EncryptionService.hash_password(password)
        
        # بررسی رمز صحیح
        self.assertTrue(EncryptionService.verify_password(password, password_hash, salt))
        
        # بررسی رمز نادرست
        self.assertFalse(EncryptionService.verify_password("wrong_password", password_hash, salt))
    
    def test_hash_consistency(self):
        """تست سازگاری هش با salt یکسان"""
        password = "test_password"
        salt = "test_salt"
        
        hash1, _ = EncryptionService.hash_password(password, salt)
        hash2, _ = EncryptionService.hash_password(password, salt)
        
        self.assertEqual(hash1, hash2)


class TestSecurityPermissions(unittest.TestCase):
    """تست مجوزها و دسترسی‌ها"""
    
    def test_file_type_validation(self):
        """تست اعتبارسنجی نوع فایل"""
        security_settings = SecuritySettings(Path("test_config.json"))
        config = security_settings.get_config()
        allowed_types = config.get("allowed_file_types", [])
        
        # تست فایل مجاز
        self.assertIn(".odt", allowed_types)
        
        # تست فایل غیرمجاز
        self.assertNotIn(".exe", allowed_types)
    
    def test_file_size_limit(self):
        """تست محدودیت اندازه فایل"""
        security_settings = SecuritySettings(Path("test_config.json"))
        config = security_settings.get_config()
        max_size = config.get("max_file_size_mb", 50)
        
        self.assertGreater(max_size, 0)
        self.assertLessEqual(max_size, 1000)  # حداکثر 1GB منطقی است


if __name__ == '__main__':
    unittest.main()




