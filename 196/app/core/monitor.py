from collections import defaultdict
from datetime import datetime, timedelta

# ذخیره‌ی فعالیت کاربران
request_log = defaultdict(list)
forbidden_log = defaultdict(list)

# محدودیت‌ها
MAX_REQUESTS_PER_MINUTE = 10
MAX_403_CONSECUTIVE = 3

def log_request(user_id: str):
    now = datetime.now()
    request_log[user_id].append(now)
    # پاکسازی قدیمی‌ها
    request_log[user_id] = [t for t in request_log[user_id] if now - t < timedelta(minutes=1)]
    if len(request_log[user_id]) > MAX_REQUESTS_PER_MINUTE:
        alert(user_id, "High request rate detected")

def log_403(user_id: str):
    now = datetime.now()
    forbidden_log[user_id].append(now)
    # فقط آخرین 403ها نگه داشته می‌شوند
    forbidden_log[user_id] = [t for t in forbidden_log[user_id] if now - t < timedelta(minutes=10)]
    if len(forbidden_log[user_id]) >= MAX_403_CONSECUTIVE:
        alert(user_id, "Multiple consecutive 403 errors")

def alert(user_id: str, message: str):
    # اینجا هشدار می‌فرستیم (الان ساده چاپ می‌کنیم)
    print(f"[ALERT] User {user_id}: {message}")
