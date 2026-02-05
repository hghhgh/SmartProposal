# Service Utilities & Health Check

این پروژه شامل چند ابزار پایه برای نگهداری و مانیتورینگ سرویس‌هاست.

---

##  Features

### 1. Automatic Cleanup of Temporary Files
- حذف خودکار فایل‌های موقت پردازش‌شده پس از `n` ساعت
- جلوگیری از پر شدن فضای دیسک
- اطمینان از عدم حذف فایل‌های اصلی

### 2. Health Check Endpoint
- ارائه route استاندارد `/health`
- بررسی پاسخ‌دهی سرویس
- مناسب برای monitoring، load balancer و CI

---

##  Project Structure

