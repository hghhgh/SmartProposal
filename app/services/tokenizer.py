"""
ماژول توکن‌سازی برای متن فارسی
"""

import re
from typing import List, Dict, Any, Tuple


class PersianTokenizer:
    """کلاس توکن‌سازی برای متن فارسی"""
    
    def __init__(self):
        # الگوهای توکن‌سازی
        self.word_pattern = re.compile(
            r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+'
        )
        self.number_pattern = re.compile(r'\d+')
        self.punctuation_pattern = re.compile(r'[^\w\s]')
        
        # نشانه‌گذاری فارسی
        self.persian_punctuation = '،؛؟!'
        
    def tokenize(self, text: str) -> List[str]:
        """
        توکن‌سازی متن فارسی
        
        Args:
            text: متن ورودی
        
        Returns:
            لیست توکن‌ها
        """
        if not text:
            return []
        
        tokens = []
        current_token = ""
        
        for char in text:
            if self._is_persian_char(char):
                if current_token and not self._is_persian_char(current_token[-1]):
                    if current_token.strip():
                        tokens.append(current_token.strip())
                    current_token = char
                else:
                    current_token += char
            elif char.isdigit():
                if current_token and not current_token[-1].isdigit():
                    if current_token.strip():
                        tokens.append(current_token.strip())
                    current_token = char
                else:
                    current_token += char
            elif char.isspace():
                if current_token.strip():
                    tokens.append(current_token.strip())
                    current_token = ""
            else:
                if current_token.strip():
                    tokens.append(current_token.strip())
                if char in self.persian_punctuation or char in '.,;:!?':
                    tokens.append(char)
                current_token = ""
        
        if current_token.strip():
            tokens.append(current_token.strip())
        
        return [token for token in tokens if token]
    
    def _is_persian_char(self, char: str) -> bool:
        """بررسی اینکه کاراکتر فارسی است یا نه"""
        return bool(re.match(r'[\u0600-\u06FF]', char))
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """
        تقسیم متن به جملات
        
        Args:
            text: متن ورودی
        
        Returns:
            لیست جملات
        """
        if not text:
            return []
        
        # الگوی پایان جمله فارسی
        sentence_endings = r'[.!?؟!]\s+'
        sentences = re.split(sentence_endings, text)
        
        # اضافه کردن نشانه پایان جمله به هر جمله
        result = []
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if sentence:
                result.append(sentence)
        
        return result
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        استخراج کلمات از متن
        
        Args:
            text: متن ورودی
        
        Returns:
            لیست کلمات
        """
        if not text:
            return []
        
        words = self.word_pattern.findall(text)
        return words
    
    def get_token_stats(self, text: str) -> Dict[str, Any]:
        """
        دریافت آمار توکن‌ها
        
        Args:
            text: متن ورودی
        
        Returns:
            دیکشنری حاوی آمار
        """
        tokens = self.tokenize(text)
        words = self.tokenize_words(text)
        sentences = self.tokenize_sentences(text)
        
        return {
            "total_tokens": len(tokens),
            "total_words": len(words),
            "total_sentences": len(sentences),
            "avg_tokens_per_sentence": round(len(tokens) / len(sentences), 2) if sentences else 0,
            "avg_words_per_sentence": round(len(words) / len(sentences), 2) if sentences else 0
        }




