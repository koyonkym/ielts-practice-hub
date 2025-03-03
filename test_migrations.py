import os
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

TEST_DB_PATH = "test_ielts_writing.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

@pytest.fixture
def setup_database():
    """Ensure a fresh database is created for each test."""
    # Remove any existing test database
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")

    # Create a SQLAlchemy session
    engine = create_engine(TEST_DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Cleanup: Close session and delete test database
    session.close()
    engine.dispose()
    os.remove(TEST_DB_PATH)

def test_migrations_apply_correctly(setup_database):
    """Verify that the tables are created after running Alembic migrations."""
    session = setup_database
    inspector = inspect(session.bind)

    # Check if tables exist
    tables = inspector.get_table_names()
    assert "questions" in tables, "Table 'questions' does not exist after migration!"
    assert "answers" in tables, "Table 'answers' does not exist after migration!"

    # Check table columns
    questions_columns = {col["name"] for col in inspector.get_columns("questions")}
    expected_questions_columns = {"id", "test_type", "task_type", "question_text"}
    assert questions_columns == expected_questions_columns, f"Unexpected columns in 'questions': {questions_columns}"

    answers_columns = {col["name"] for col in inspector.get_columns("answers")}
    expected_answers_columns = {"id", "question_id", "answer_text", "reference_url"}
    assert answers_columns == expected_answers_columns, f"Unexpected columns in 'answers': {answers_columns}"

def test_foreign_keys_exist(setup_database):
    """Ensure foreign keys are correctly set up."""
    session = setup_database
    inspector = inspect(session.bind)

    fks = inspector.get_foreign_keys("answers")
    assert len(fks) == 1, "No foreign key found in 'answers' table!"
    assert fks[0]["referred_table"] == "questions", "Foreign key does not reference 'questions' table!"
