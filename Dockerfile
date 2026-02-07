# Dockerfile اصلی برای SmartProposal
# استفاده از Python 3.10 slim برای کاهش حجم
FROM python:3.10-slim

# تنظیم متغیرهای محیطی
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# ایجاد دایرکتوری کار
WORKDIR /app

# کپی فایل requirements و نصب وابستگی‌ها
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# کپی کد برنامه
COPY app/ ./app/
COPY samples/ ./samples/

# ایجاد دایرکتوری‌های لازم
RUN mkdir -p uploads && \
    chmod 755 uploads

# پورت پیش‌فرض
EXPOSE 8000

# اجرای برنامه با uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




