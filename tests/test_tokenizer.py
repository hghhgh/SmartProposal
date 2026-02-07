"""
تست‌های واحد برای ماژول tokenizer
"""

import unittest
from app.services.tokenizer import PersianTokenizer


class TestPersianTokenizer(unittest.TestCase):
    """تست‌های کلاس PersianTokenizer"""
    
    def setUp(self):
        """تنظیمات اولیه برای هر تست"""
        self.tokenizer = PersianTokenizer()
    
    def test_tokenize_simple_text(self):
        """تست توکن‌سازی متن ساده"""
        text = "این یک متن تست است."
        tokens = self.tokenizer.tokenize(text)
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)
        self.assertIn("این", tokens)
        self.assertIn("یک", tokens)
    
    def test_tokenize_empty_text(self):
        """تست توکن‌سازی متن خالی"""
        text = ""
        tokens = self.tokenizer.tokenize(text)
        self.assertEqual(tokens, [])
    
    def test_tokenize_with_punctuation(self):
        """تست توکن‌سازی با نشانه‌گذاری"""
        text = "سلام، چطوری؟ خوبی!"
        tokens = self.tokenizer.tokenize(text)
        self.assertIn("،", tokens)
        self.assertIn("؟", tokens)
        self.assertIn("!", tokens)
    
    def test_tokenize_with_numbers(self):
        """تست توکن‌سازی با اعداد"""
        text = "این متن شامل 123 عدد است."
        tokens = self.tokenizer.tokenize(text)
        self.assertIn("123", tokens)
    
    def test_tokenize_sentences(self):
        """تست تقسیم به جملات"""
        text = "این جمله اول است. این جمله دوم است؟ و این جمله سوم!"
        sentences = self.tokenizer.tokenize_sentences(text)
        self.assertEqual(len(sentences), 3)
        self.assertIn("این جمله اول است", sentences[0])
    
    def test_tokenize_words(self):
        """تست استخراج کلمات"""
        text = "این یک متن فارسی است"
        words = self.tokenizer.tokenize_words(text)
        self.assertIsInstance(words, list)
        self.assertGreater(len(words), 0)
        self.assertTrue(all(self.tokenizer._is_persian_char(word[0]) for word in words if word))
    
    def test_get_token_stats(self):
        """تست دریافت آمار توکن‌ها"""
        text = "این یک متن تست است. این جمله دوم است."
        stats = self.tokenizer.get_token_stats(text)
        
        self.assertIn("total_tokens", stats)
        self.assertIn("total_words", stats)
        self.assertIn("total_sentences", stats)
        self.assertIn("avg_tokens_per_sentence", stats)
        self.assertIn("avg_words_per_sentence", stats)
        
        self.assertGreater(stats["total_tokens"], 0)
        self.assertGreater(stats["total_words"], 0)
        self.assertGreater(stats["total_sentences"], 0)
    
    def test_tokenize_complex_text(self):
        """تست توکن‌سازی متن پیچیده"""
        text = "این یک متن پیچیده است که شامل اعداد 123 و نشانه‌گذاری،؛؟ است."
        tokens = self.tokenizer.tokenize(text)
        self.assertGreater(len(tokens), 5)
    
    def test_is_persian_char(self):
        """تست تشخیص کاراکتر فارسی"""
        self.assertTrue(self.tokenizer._is_persian_char("ا"))
        self.assertTrue(self.tokenizer._is_persian_char("ب"))
        self.assertFalse(self.tokenizer._is_persian_char("a"))
        self.assertFalse(self.tokenizer._is_persian_char("1"))


if __name__ == '__main__':
    unittest.main()




