import sqlite3
import streamlit as st

DB_NAME = st.session_state.get("db_name", "ielts_writing.db")

def add_question_with_answer(question_text: str, task_type: str, answer_text: str, reference_url: str, db_name=DB_NAME):
    """Insert a question and its answer into the database in one transaction."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert the question
    cursor.execute("INSERT INTO questions (question_text, task_type) VALUES (?, ?)", (question_text, task_type))
    question_id = cursor.lastrowid

    # Insert the answer linked to the question
    cursor.execute("INSERT INTO answers (question_id, answer_text, reference_url) VALUES (?, ?, ?)", (question_id, answer_text, reference_url))

    conn.commit()
    conn.close()

def get_all_entries(db_name=DB_NAME):
    """Retrieve all questions with their corresponding answers."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            q.id,
            q.question_text,
            q.task_type,
            a.answer_text,
            a.reference_url
        FROM
            questions q
        LEFT JOIN
            answers a
        ON
            q.id = a.question_id
        ORDER BY
            q.id DESC
    """)
    entries = cursor.fetchall()
    conn.close()
    return entries

# Streamlit UI
st.title("IELTS Writing Data Entry")

# Section to add a new question and answer
st.header("Add a New Question & Answer")
question_text = st.text_area("Question Text", key="question_text")
task_type = st.selectbox("Task Type", ["Task 1", "Task 2"], key="task_type")
answer_text = st.text_area("Answer Text", key="answer_text")
reference_url = st.text_input("Reference URL (optional)", key="reference_url")

if st.button("Add Question & Answer", key="add_q_and_a"):
    if question_text and answer_text:
        add_question_with_answer(question_text, task_type, answer_text, reference_url)
        st.success("Question and Answer added successfully!")
    else:
        st.warning("Please enter both a question and an answer.")

# Display existing entries
st.header("Existing Questions & Answers")
entries = get_all_entries()
if entries:
    for q_id, q_text, q_task, a_text, ref_url in entries:
        st.markdown(f"### 📝 {q_text} ({q_task})")
        st.write(f"**Answer:** {a_text}")
        if ref_url:
            st.write(f"[Reference]({ref_url})")
        st.markdown("---")
else:
    st.info("No entries available. Please add a question and answer first.")
