import sqlite3

def initialize_database(db_name="ielts_writing.db"):
    """Initialize the database with the given name."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL,
        task_type TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        answer_text TEXT NOT NULL,
        reference_url TEXT,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
