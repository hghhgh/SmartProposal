"""
ماژول تشخیص bias داده
"""

from typing import List, Dict, Any
import re
from app.utils.file_manager import FileManager


class BiasDetectionService:
    """سرویس تشخیص bias در داده‌ها"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        
        # الگوهای bias احتمالی
        self.gender_biased_words = {
            "مردانه": ["مرد", "آقا", "پسر", "پدر"],
            "زنانه": ["زن", "خانم", "دختر", "مادر"]
        }
        
        self.age_biased_words = ["جوان", "پیر", "مسن", "نوجوان"]
        
        self.socioeconomic_biased_words = ["ثروتمند", "فقیر", "غنی", "محتاج"]
    
    def detect_bias(self, file_id: str) -> Dict[str, Any]:
        """
        تشخیص bias در فایل
        
        Args:
            file_id: شناسه فایل
        
        Returns:
            دیکشنری حاوی نتایج تشخیص bias
        """
        file_info = self.file_manager.get_file_info(file_id)
        if not file_info:
            raise ValueError(f"فایل با شناسه {file_id} یافت نشد")
        
        # دریافت متن پاکسازی شده
        cleaned_text = file_info.get("cleaned_text", "")
        if not cleaned_text:
            # اگر متن پاکسازی شده وجود ندارد، باید استخراج شود
            # در اینجا برای سادگی، از متن خام استفاده می‌کنیم
            cleaned_text = ""
        
        bias_types = []
        bias_details = []
        
        # بررسی gender bias
        gender_bias = self._detect_gender_bias(cleaned_text)
        if gender_bias["has_bias"]:
            bias_types.append("gender")
            bias_details.append(gender_bias)
        
        # بررسی age bias
        age_bias = self._detect_age_bias(cleaned_text)
        if age_bias["has_bias"]:
            bias_types.append("age")
            bias_details.append(age_bias)
        
        # بررسی socioeconomic bias
        socioeconomic_bias = self._detect_socioeconomic_bias(cleaned_text)
        if socioeconomic_bias["has_bias"]:
            bias_types.append("socioeconomic")
            bias_details.append(socioeconomic_bias)
        
        # بررسی linguistic bias
        linguistic_bias = self._detect_linguistic_bias(cleaned_text)
        if linguistic_bias["has_bias"]:
            bias_types.append("linguistic")
            bias_details.append(linguistic_bias)
        
        # تولید توصیه‌ها
        recommendations = self._generate_recommendations(bias_types, bias_details)
        
        return {
            "file_id": file_id,
            "has_bias": len(bias_types) > 0,
            "bias_types": bias_types,
            "bias_details": bias_details,
            "recommendations": recommendations
        }
    
    def _detect_gender_bias(self, text: str) -> Dict[str, Any]:
        """تشخیص gender bias"""
        male_count = sum(len(re.findall(word, text, re.IGNORECASE)) for word in self.gender_biased_words["مردانه"])
        female_count = sum(len(re.findall(word, text, re.IGNORECASE)) for word in self.gender_biased_words["زنانه"])
        
        total_gender_words = male_count + female_count
        if total_gender_words == 0:
            return {"has_bias": False, "type": "gender"}
        
        male_ratio = male_count / total_gender_words
        female_ratio = female_count / total_gender_words
        
        # اگر تفاوت بیشتر از 70% باشد، bias وجود دارد
        has_bias = abs(male_ratio - female_ratio) > 0.7
        
        return {
            "has_bias": has_bias,
            "type": "gender",
            "male_count": male_count,
            "female_count": female_count,
            "male_ratio": round(male_ratio, 2),
            "female_ratio": round(female_ratio, 2),
            "description": "عدم تعادل در استفاده از کلمات مرتبط با جنسیت"
        }
    
    def _detect_age_bias(self, text: str) -> Dict[str, Any]:
        """تشخیص age bias"""
        age_word_count = sum(len(re.findall(word, text, re.IGNORECASE)) for word in self.age_biased_words)
        
        has_bias = age_word_count > 5  # اگر بیش از 5 بار از کلمات مرتبط با سن استفاده شده
        
        return {
            "has_bias": has_bias,
            "type": "age",
            "age_word_count": age_word_count,
            "description": "استفاده بیش از حد از کلمات مرتبط با سن"
        }
    
    def _detect_socioeconomic_bias(self, text: str) -> Dict[str, Any]:
        """تشخیص socioeconomic bias"""
        socioeconomic_word_count = sum(
            len(re.findall(word, text, re.IGNORECASE)) 
            for word in self.socioeconomic_biased_words
        )
        
        has_bias = socioeconomic_word_count > 3
        
        return {
            "has_bias": has_bias,
            "type": "socioeconomic",
            "word_count": socioeconomic_word_count,
            "description": "استفاده از کلمات مرتبط با وضعیت اقتصادی-اجتماعی"
        }
    
    def _detect_linguistic_bias(self, text: str) -> Dict[str, Any]:
        """تشخیص linguistic bias (مثلاً استفاده بیش از حد از کلمات خاص)"""
        # این یک نمونه ساده است
        words = text.split()
        if len(words) == 0:
            return {"has_bias": False, "type": "linguistic"}
        
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # اگر یک کلمه بیش از 10% متن را تشکیل دهد
        max_freq = max(word_freq.values()) if word_freq else 0
        max_ratio = max_freq / len(words) if words else 0
        
        has_bias = max_ratio > 0.1
        
        return {
            "has_bias": has_bias,
            "type": "linguistic",
            "max_word_frequency": max_freq,
            "max_word_ratio": round(max_ratio, 2),
            "description": "استفاده بیش از حد از یک کلمه خاص"
        }
    
    def _generate_recommendations(self, bias_types: List[str], bias_details: List[Dict[str, Any]]) -> List[str]:
        """تولید توصیه‌ها برای کاهش bias"""
        recommendations = []
        
        if "gender" in bias_types:
            recommendations.append("سعی کنید از کلمات خنثی از نظر جنسیت استفاده کنید.")
            recommendations.append("از تعادل در استفاده از کلمات مرتبط با جنسیت اطمینان حاصل کنید.")
        
        if "age" in bias_types:
            recommendations.append("از استفاده بیش از حد از کلمات مرتبط با سن خودداری کنید.")
        
        if "socioeconomic" in bias_types:
            recommendations.append("از کلمات خنثی‌تر برای توصیف وضعیت اقتصادی-اجتماعی استفاده کنید.")
        
        if "linguistic" in bias_types:
            recommendations.append("تنوع بیشتری در استفاده از کلمات ایجاد کنید.")
        
        if not recommendations:
            recommendations.append("هیچ bias قابل توجهی تشخیص داده نشد.")
        
        return recommendations




