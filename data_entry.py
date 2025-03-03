from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import streamlit as st
from models import Question, Answer, Base

# Define the database URL
DB_URL = "sqlite:///ielts_writing.db"

# Create an engine and session factory
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)

def get_session():
    """Create and return a new SQLAlchemy session."""
    return Session(bind=engine)

def add_question_with_answer(session: Session, test_type: str, task_type:str, question_text: str, answer_text: str, reference_url: str):
    """Insert a question and its answer into the database using SQLAlchemy ORM."""
    question = Question(test_type=test_type, task_type=task_type, question_text=question_text)
    session.add(question)
    session.flush()

    answer = Answer(question_id=question.id, answer_text=answer_text, reference_url=reference_url)
    session.add(answer)

    session.commit()

def get_all_entries(session: Session):
    """Retrieve all questions with their corresponding answers using SQLAlchemy ORM."""
    entries = (
        session.query(Question.id, Question.test_type, Question.task_type, Question.question_text, Answer.answer_text, Answer.reference_url)
        .outerjoin(Answer, Question.id == Answer.question_id)
        .order_by(Question.id.desc())
        .all()
    )
    return [
        {
            "id": entry[0],
            "test_type": entry[1],
            "task_type": entry[2],
            "question_text": entry[3],
            "answer_text": entry[4],
            "reference_url": entry[5] if entry[5] else None
        }
        for entry in entries
    ]

# Streamlit UI
st.title("IELTS Writing Data Entry")

# Create a session
session = get_session()

# Section to add a new question and answer
st.header("Add a New Question & Answer")
test_type = st.selectbox("Test Type", ["Academic", "General Training"], key="test_type")
task_type = st.selectbox("Task Type", ["Task 1", "Task 2"], key="task_type")
question_text = st.text_area("Question Text", key="question_text")
answer_text = st.text_area("Answer Text", key="answer_text")
reference_url = st.text_input("Reference URL (optional)", key="reference_url")

if st.button("Add Question & Answer", key="add_q_and_a"):
    if question_text and answer_text:
        add_question_with_answer(session, test_type, task_type, question_text, answer_text, reference_url)
        st.success("Question and Answer added successfully!")
    else:
        st.warning("Please enter both a question and an answer.")

# Display existing entries
st.header("Existing Questions & Answers")
entries = get_all_entries(session)
if entries:
    for entry in entries:
        st.markdown(f"### 📝 {entry['question_text']} ({entry['test_type']}, {entry['task_type']})")
        st.write(f"**Answer:** {entry['answer_text']}")
        if entry["reference_url"]:
            st.write(f"[Reference]({entry['reference_url']})")
        st.markdown("---")
else:
    st.info("No entries available. Please add a question and answer first.")

# Close the session
session.close()
