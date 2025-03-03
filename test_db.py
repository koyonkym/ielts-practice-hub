import sqlite3
import os
import pytest
from init_db import initialize_database
from data_entry import add_question_with_answer, get_all_entries

TEST_DB = "test_ielts_writing.db"

@pytest.fixture
def setup_test_db():
    """Setup a temporary test database."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    initialize_database(TEST_DB)
    yield

def test_add_question_with_answer(setup_test_db):
    """Test inserting a question with an answer."""
    conn = sqlite3.connect(TEST_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.close()

    add_question_with_answer("What is your favorite book?", "Task 2", "My favorite book is...", "https://example.com", TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    assert len(questions) == 1
    assert questions[0][1] == "What is your favorite book?"

    cursor.execute("SELECT * FROM answers")
    answers = cursor.fetchall()
    assert len(answers) == 1
    assert answers[0][2] == "My favorite book is..."
    assert answers[0][3] == "https://example.com"

    conn.close()

def test_get_all_entries(setup_test_db):
    """Test fetching questions and answers."""
    add_question_with_answer("Describe your city.", "Task 1", "My city is beautiful.", "https://city.com", TEST_DB)

    entries = get_all_entries(TEST_DB)
    assert len(entries) == 1
    assert entries[0][1] == "Describe your city."
    assert entries[0][3] == "My city is beautiful."
