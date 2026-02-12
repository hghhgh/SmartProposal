from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

# تعریف مدل بازخورد
class Feedback(BaseModel):
    user_id: str
    proposal_text: str
    feedback_text: str
    label: str = "unlabeled"  # می‌تونه optional باشه

app = FastAPI()

DB_PATH = "smartproposal.db"

# ساخت جدول اگر وجود نداشته باشه
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS labeled_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        proposal_text TEXT NOT NULL,
        feedback_text TEXT NOT NULL,
        label TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()

# API برای دریافت batch بازخورد
@app.post("/feedback/collect")
def collect_feedback(batch: List[Feedback]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for fb in batch:
        cursor.execute("""
        INSERT INTO labeled_feedback (user_id, proposal_text, feedback_text, label)
        VALUES (?, ?, ?, ?)
        """, (fb.user_id, fb.proposal_text, fb.feedback_text, fb.label))

    conn.commit()
    conn.close()
    return {"status": "success", "count": len(batch)}

# تست سریع
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
