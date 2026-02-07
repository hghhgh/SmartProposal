"""
ماژول آماده‌سازی داده (Data Cleaning Module)
این ماژول وظایف پاکسازی و نرمال‌سازی متن فارسی را انجام می‌دهد.
"""

import re
import unicodedata
from typing import List, Dict, Any


class DataCleaning:
    """کلاس اصلی برای پاکسازی و نرمال‌سازی داده‌های فارسی"""
    
    def __init__(self):
        # الگوهای کاراکترهای غیرضروری
        self.extra_spaces_pattern = re.compile(r'\s+')
        self.zero_width_pattern = re.compile(r'[\u200B-\u200D\uFEFF]')
        
        # کاراکترهای نشانه‌گذاری فارسی
        self.persian_punctuation = '،؛؟'
        self.english_punctuation = ',;?'
        
    def normalize_unicode(self, text: str) -> str:
        """
        نرمال‌سازی یونیکد متن فارسی
        تبدیل کاراکترهای مشابه به یک فرم استاندارد
        """
        if not text:
            return ""
        
        # حذف کاراکترهای Zero-Width
        text = self.zero_width_pattern.sub('', text)
        
        # نرمال‌سازی یونیکد (NFKC)
        text = unicodedata.normalize('NFKC', text)
        
        return text
    
    def normalize_persian_chars(self, text: str) -> str:
        """
        نرمال‌سازی کاراکترهای فارسی
        تبدیل انواع مختلف یک کاراکتر به فرم استاندارد
        """
        if not text:
            return ""
        
        # تبدیل انواع مختلف کاف و ی
        replacements = {
            'ك': 'ک',
            'ي': 'ی',
            'ة': 'ه',
            'أ': 'ا',
            'إ': 'ا',
            'آ': 'آ',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def normalize_whitespace(self, text: str) -> str:
        """
        نرمال‌سازی فاصله‌ها
        حذف فاصله‌های اضافی و نرمال‌سازی
        """
        if not text:
            return ""
        
        # حذف فاصله‌های اضافی
        text = self.extra_spaces_pattern.sub(' ', text)
        
        # حذف فاصله قبل از نشانه‌گذاری
        text = re.sub(r'\s+([،؛؟!])', r'\1', text)
        
        # اضافه کردن فاصله بعد از نشانه‌گذاری (در صورت نیاز)
        text = re.sub(r'([،؛؟!])([^\s])', r'\1 \2', text)
        
        return text.strip()
    
    def remove_extra_newlines(self, text: str) -> str:
        """
        حذف خطوط خالی اضافی
        """
        if not text:
            return ""
        
        # تبدیل چندین خط خالی به حداکثر دو خط
        text = re.sub(r'\n{3,}', r'\n\n', text)
        
        return text
    
    def clean_text(self, text: str, 
                   normalize_unicode: bool = True,
                   normalize_persian: bool = True,
                   normalize_whitespace: bool = True,
                   remove_extra_newlines: bool = True) -> str:
        """
        پاکسازی کامل متن با استفاده از تمام روش‌های نرمال‌سازی
        
        Args:
            text: متن ورودی
            normalize_unicode: نرمال‌سازی یونیکد
            normalize_persian: نرمال‌سازی کاراکترهای فارسی
            normalize_whitespace: نرمال‌سازی فاصله‌ها
            remove_extra_newlines: حذف خطوط خالی اضافی
        
        Returns:
            متن پاکسازی شده
        """
        if not text:
            return ""
        
        cleaned_text = text
        
        if normalize_unicode:
            cleaned_text = self.normalize_unicode(cleaned_text)
        
        if normalize_persian:
            cleaned_text = self.normalize_persian_chars(cleaned_text)
        
        if normalize_whitespace:
            cleaned_text = self.normalize_whitespace(cleaned_text)
        
        if remove_extra_newlines:
            cleaned_text = self.remove_extra_newlines(cleaned_text)
        
        return cleaned_text
    
    def clean_batch(self, texts: List[str], **kwargs) -> List[str]:
        """
        پاکسازی دسته‌ای متون
        
        Args:
            texts: لیست متون
            **kwargs: پارامترهای پاکسازی
        
        Returns:
            لیست متون پاکسازی شده
        """
        return [self.clean_text(text, **kwargs) for text in texts]
    
    def get_cleaning_stats(self, original_text: str, cleaned_text: str) -> Dict[str, Any]:
        """
        دریافت آمار پاکسازی
        
        Args:
            original_text: متن اصلی
            cleaned_text: متن پاکسازی شده
        
        Returns:
            دیکشنری حاوی آمار
        """
        return {
            "original_length": len(original_text),
            "cleaned_length": len(cleaned_text),
            "removed_chars": len(original_text) - len(cleaned_text),
            "removal_percentage": round(
                (len(original_text) - len(cleaned_text)) / len(original_text) * 100, 2
            ) if original_text else 0
        }




