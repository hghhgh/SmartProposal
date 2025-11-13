import logging
import re
import time
from datetime import datetime


logging.basicConfig(
    filename="extract_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def count_paragraphs(text):
  
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    return len(paragraphs)

def count_tables(text):
  
    table_pattern = r"(\|.+\|)|(-{3,})"
    tables = re.findall(table_pattern, text)
    return len(tables)

def process_text_file(file_path):
    logging.info("شروع فرآیند استخراج")

    start_time = time.time()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        paragraph_count = count_paragraphs(text)
        table_count = count_tables(text)

       
        error_pattern = r"(ERROR|Exception)"
        errors = re.findall(error_pattern, text, re.IGNORECASE)
        error_count = len(errors)

        end_time = time.time()
        duration = end_time - start_time

        logging.info(f"تعداد پاراگراف‌ها: {paragraph_count}")
        logging.info(f"تعداد جدول‌ها: {table_count}")
        logging.info(f"تعداد خطاها: {error_count}")
        logging.info(f"زمان شروع: {datetime.fromtimestamp(start_time)}")
        logging.info(f"زمان پایان: {datetime.fromtimestamp(end_time)}")
        logging.info(f"مدت زمان اجرا: {duration:.2f} ثانیه")

        print("✅ عملیات با موفقیت انجام شد. نتیجه در فایل 'extract_log.txt' ثبت شد.")

    except Exception as e:
        logging.error(f"خطا در پردازش فایل: {e}")
        print("❌ خطایی رخ داد. جزئیات در فایل لاگ ثبت شده است.")

if __name__ == "__main__":
    file_path = "input.txt" 
    process_text_file(file_path)
