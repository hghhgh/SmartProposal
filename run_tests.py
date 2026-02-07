#!/usr/bin/env python3
"""
اسکریپت اجرای تست‌ها
"""

import unittest
import sys
from pathlib import Path

# اضافه کردن مسیر پروژه به sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# پیدا کردن و بارگذاری تمام تست‌ها
def load_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    from tests.test_tokenizer import TestPersianTokenizer
    suite.addTests(loader.loadTestsFromTestCase(TestPersianTokenizer))
    
   
    try:
        from tests.test_security import (
            TestSecuritySettings, TestEncryptionService, TestSecurityPermissions
        )
        suite.addTests(loader.loadTestsFromTestCase(TestSecuritySettings))
        suite.addTests(loader.loadTestsFromTestCase(TestEncryptionService))
        suite.addTests(loader.loadTestsFromTestCase(TestSecurityPermissions))
    except ImportError as e:
        print(f"Warning: Could not load security tests: {e}")
    
    # penetration
    try:
        from tests.test_pentest import TestPenetrationTesting
        suite.addTests(loader.loadTestsFromTestCase(TestPenetrationTesting))
    except ImportError as e:
        print(f"Warning: Could not load penetration tests: {e}")
    
    return suite

if __name__ == '__main__':
    suite = load_tests()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    sys.exit(0 if result.wasSuccessful() else 1)




