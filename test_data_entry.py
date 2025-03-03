import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from alembic.config import Config
from alembic import command
from data_entry import add_question_with_answer, get_all_entries

TEST_DB_PATH = "test_ielts_writing.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

@pytest.fixture(scope="function")
def setup_test_db():
    """Setup a temporary test database with Alembic migrations."""
    # Remove old test database
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")

    # Create SQLAlchemy session
    engine = create_engine(TEST_DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Cleanup
    session.close()
    engine.dispose()
    os.remove(TEST_DB_PATH)

def test_add_question_with_answer(setup_test_db):
    """Test inserting a question with an answer."""
    session = setup_test_db

    add_question_with_answer(session, "Academic", "Task 2", "What is your favorite book?", "My favorite book is...", "https://example.com")

    # Verify inserted data
    entries = get_all_entries(session)
    assert len(entries) == 1
    assert entries[0]["question_text"] == "What is your favorite book?"
    assert entries[0]["answer_text"] == "My favorite book is..."
    assert entries[0]["reference_url"] == "https://example.com"

def test_get_all_entries(setup_test_db):
    """Test fetching questions and answers."""
    session = setup_test_db

    add_question_with_answer(session, "General Training", "Task 1", "Describe your city.", "My city is beautiful.", "https://city.com")

    entries = get_all_entries(session)
    assert len(entries) == 1
    assert entries[0]["question_text"] == "Describe your city."
    assert entries[0]["answer_text"] == "My city is beautiful."
    assert entries[0]["reference_url"] == "https://city.com"
