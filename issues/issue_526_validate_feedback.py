import json

def load_feedback(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_feedback(data):
    valid_feedback = []

    for item in data:
        if not item.get("user_id"):
            continue  # رد بازخورد بدون کاربر
        if not item.get("proposal_text"):
            continue  # رد بازخورد بدون متن
        if not item.get("feedback"):
            continue  # رد بازخورد بدون پاسخ

        # اینجا می‌تونیم تست‌های پیچیده‌تر اضافه کنیم
        # مثلاً تناقض در پاسخ، طول خیلی کم/خیلی زیاد و غیره

        valid_feedback.append(item)

    return valid_feedback

def save_valid_feedback(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    raw_data = load_feedback("raw_feedback.json")
    cleaned_data = validate_feedback(raw_data)
    save_valid_feedback(cleaned_data, "valid_feedback.json")
    print(f" Valid feedback saved. Total: {len(cleaned_data)} items")
