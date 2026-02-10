import pandas as pd 
from langdetect import detect # LangDetect: کتابخانه تشخیص خودکار زبان متن
from hazm import Normalizer, word_tokenize # _Hazm_Tools: ابزار استاندارد برای پیش‌پردازش متون فارسی
import statistics #  برای محاسبات آماری

class DatasetQualityAudit:
    def __init__(self, file_path, text_column):
        # بارگذاری میکنیم فایل دیتاست را در حافظه
        self.df = pd.read_csv(file_path)
        # ستونی که میخواهیم آن را بررسی کنیم تعیین میکنیم
        self.text_col = text_column
        #    یک دیکشنری خالی برای بررسی تست ها میسازیم
        self.report = {}

    def check_language_consistency(self):
       # در این قسمت بررسی میکنیم: میزان انطباق زبان دیتاست با زبان مقصد (فارسی)
        #  تعریف یک تابع داخلی برای تشخیص زبان تک‌تک ردیف‌ها
        def is_persian(text):
            try:
                #    را بگردانtrue اگر زبان تشخیص داده شده مقدار fa (Persian)   
                return detect(str(text)) == 'fa'
            except:
                #  در صورت برخورد با اعداد یا کاراکترهای نامفهوم، False برمی‌گرداند
                return False
        
        #  اجرای تابع تشخیص زبان روی تمام ردیف‌های ستون متن
        results = self.df[self.text_col].apply(is_persian)
        # Calculate_Ratio: محاسبه میانگین موارد فارسی و تبدیل آن به درصد (Score 0-100)
        self.report['persian_ratio'] = results.mean() * 100
        print(f"میزان انطباق با زبان فارسی: {self.report['persian_ratio']:.2f}%")

    def check_lexical_diversity(self):
        #بررسی  لغوی برای جلوگیری از تکراری بودن داده‌ها 
        # #13_Hazm_Normalizer: ایجاد شیء نرمال‌ساز برای یکسان‌سازی کاراکترها )
        normalizer = Normalizer()
        all_words = []
        
        # در اینجا داریم: پیمایش تمام متن‌های دیتاست
        for text in self.df[self.text_col]:
            # _Tokenization: ابتدا نرمال‌سازی و سپس تبدیل متن به کلمات جداگانه (Token)
            tokens = word_tokenize(normalizer.normalize(str(text)))
            # _Extend_List: اضافه کردن کلمات متن فعلی به لیست کل کلمات دیتاست
            all_words.extend(tokens)
            
        # #17_Unique_Words:  استفاده میکنیمset ا   برای حذف کلمات تکراری و شمارش کلمات منحصربه‌فرداز
        unique_words = set(all_words)
        # _TTR_Formula: محاسبه نسبت کلمات منحصربه‌فرد به کل کلمات (Type-Token Ratio)
        diversity_score = len(unique_words) / len(all_words) if all_words else 0
        self.report['lexical_diversity'] = diversity_score
        print(f"شاخص تنوع لغوی: {diversity_score:.4f}")

    def detect_outliers(self):
        #شناسایی متون خیلی کوتاه یا خیلی بلند که نویز محسوب می‌شوند 
        # _Get_Lengths: محاسبه طول (تعداد کاراکتر) هر ردیف از متن
        lengths = self.df[self.text_col].str.len()
        # _Mean_and_Std: محاسبه میانگین و انحراف معیار طول متون
        mean_len = lengths.mean()
        std_len = lengths.std()
        
        outliers = self.df[abs(lengths - mean_len) > 3 * std_len]
        # Outlier_Count:ذخیره تعداد داده‌های پرت ی
        self.report['outliers_count'] = len(outliers)
        print(f"تعداد داده‌های پرت (Outliers): {len(outliers)}")

    def final_grade(self):
        # سیستم امتیازدهی نهایی داریم (Weighting System) برای رد یا تایید دیتاست
        score = 0
        #  در اینجا باید امتیازدهی بر اساس متریک‌های به دست آمده در مراحل قبل دهیم
        if self.report.get('persian_ratio', 0) > 90: score += 40 # وزن بالای زبان فارسی
        if self.report.get('lexical_diversity', 0) > 0.05: score += 30 # وزن تنوع لغات
        if (self.report.get('outliers_count', 0) / len(self.df)) < 0.05: score += 30 # وزن تمیز بودن داده
        
        print(f"\nامتیاز نهایی کیفیت دیتاست: {score}/100")
