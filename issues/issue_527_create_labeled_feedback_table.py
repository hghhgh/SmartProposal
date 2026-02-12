import sqlite3

def create_database():
    conn = sqlite3.connect("smartproposal.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS labeled_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proposal_text TEXT NOT NULL,
        feedback_text TEXT NOT NULL,
        label TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("✅ Table 'labeled_feedback' created successfully.")
