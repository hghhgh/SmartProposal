#داده پرت در متن یعنی جملاتی که از نظر ساختار، محتوا یا طول، شباهتی به بقیه دیتاست ندارند (مثل کدهای برنامه‌نویسی وسط یک متن ادبی، یا جملات تکراری بی‌معنی).
#از آنجا که الگوریتم‌های ریاضی متن را نمی‌فهمند، ابتدا باید متن را با TfidfVectorizer به عدد (بردار) تبدیل کنیم.

import pandas as pd 
from sklearn.ensemble import IsolationForest # #2_Isolation_Forest: الگوریتم هوشمند برای شناسایی داده‌های غیرعادی (پرت)
from sklearn.feature_extraction.text import TfidfVectorizer #  تبدیل کلمات متنی به بردارهای عددی قابل فهم برای مدل ریاضی

class TextOutlierDetector:
    def __init__(self, file_path, column_name):
        # دیتاست را باید در ایتدا بارگذاری کنیم
        self.df = pd.read_csv(file_path)
        #  مشخص کردن نام ستونی که قرار است محتوای آن بررسی شود
        self.column = column_name
        # با استفاده از متد dropna حذف ردیف‌های کاملاً خالی برای جلوگیری از بروز خطا در محاسبات مدل
        self.df = self.df.dropna(subset=[self.column])

    def detect_outliers(self):
        #در این قسمت شناساس داده ها نمونه های غیرعادی داریم با استفاده از مدل ریاضی
        print(f"--- Processing {len(self.df)} samples ---")

        # : تنظیم استخراج‌کننده ویژگی؛ تبدیل متن fi ویژگی عددی مهم
        vectorizer = TfidfVectorizer(max_features=500)
        # _Vectorization: اجرای فرآیند تبدیل متن‌ها به یک ماتریس عددی (Matrix)
        matrix = vectorizer.fit_transform(self.df[self.column])

        # 9_Model_Init: مقداردهی اولیه الگوریتم؛ تعیین اینکه ۵ درصد داده‌ها احتمالا پرت هستند (Contamination)
        model = IsolationForest(contamination=0.05, random_state=42)

        # _Prediction: آموزش مدل و پیش‌بینی وضعیت هر ردیف (1 برای نرمال، -1 برای پرت) داریم 
        self.df['anomaly_score'] = model.fit_predict(matrix.toarray())

        # : جدا کردن ردیف‌هایی که مدل آن‌ها را با امتیاز -1 (غیرعادی) تشخیص داده است
        outliers = self.df[self.df['anomaly_score'] == -1]
        
        print(f"Detected {len(outliers)} potential outliers.")
        # بازگرداندن لیست داده‌های پرت برای بررسی نهایی
        return outliers


