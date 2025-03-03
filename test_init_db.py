import sqlite3
import os
import pytest
from init_db import initialize_database

DB_PATH = "test_ielts_writing.db"

@pytest.fixture
def setup_db():
    """Ensure the test database is initialized before running tests."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    initialize_database(DB_PATH)

def test_database_exists(setup_db):
    """Check if the test database file was created."""
    assert os.path.exists(DB_PATH)

def test_tables_exist(setup_db):
    """Verify that required tables exist in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='questions'")
    assert cursor.fetchone() is not None, "Table 'questions' does not exist"

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answers'")
    assert cursor.fetchone() is not None, "Table 'answers' does not exist"

    conn.close()

def test_schema_correct(setup_db):
    """Ensure tables have the correct schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check 'questions' table
    cursor.execute("PRAGMA table_info(questions)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    assert columns == {
        "id": "INTEGER",
        "question_text": "TEXT",
        "task_type": "TEXT"
    }, f"Unexpected schema for 'questions': {columns}"

    # Check 'answers' table
    cursor.execute("PRAGMA table_info(answers)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    assert "reference_url" in columns, "'reference_url' column is missing in 'answers'"

    conn.close()
