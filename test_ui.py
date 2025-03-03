import os
from streamlit.testing.v1 import AppTest

TEST_DB_NAME = "test_ielts_writing.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_NAME}"

def initialize_test_db():
    """Set up a test database with required tables using SQLAlchemy."""
    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)

def test_streamlit_ui():
    initialize_test_db()

    app = AppTest.from_file("data_entry.py")
    app.session_state["db_url"] = TEST_DB_URL

    # Check title exists
    app.run()
    assert app.title[0].value == "IELTS Writing Data Entry"

    # Simulate user input
    app.selectbox("test_type").select("Academic").run()
    app.selectbox("task_type").select("Task 1").run()
    app.text_area("question_text").input("What is your hobby?").run()
    app.text_area("answer_text").input("I love playing piano.").run()
    app.text_input("reference_url").input("https://hobby.com").run()

    # Click button
    app.button("add_q_and_a").click().run()

    # Verify success message
    assert app.success[0].value == "Question and Answer added successfully!"

    os.remove(TEST_DB_NAME)
