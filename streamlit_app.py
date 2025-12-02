# streamlit_app.py
import streamlit as st
import os
from utils import generate_questions, evaluate_answer

st.set_page_config(page_title="AI Interview Bot", layout="wide")

# Load API key from Streamlit Secrets
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.error("⚠️ Missing OPENAI_API_KEY in Streamlit Secrets!")
    st.stop()

st.title("🤖 AI Interview Bot")
st.write("Generate mock interview questions & evaluate your answers.")

# --- Sidebar for inputs ---
st.sidebar.header("Interview Settings")

role = st.sidebar.text_input("Job Role", "Software Engineer")
skill = st.sidebar.text_input("Primary Skill", "Python")
n_questions = st.sidebar.slider("Number of Questions", 1, 10, 5)

if st.sidebar.button("Generate Questions"):
    st.session_state.questions = generate_questions(role, skill, n_questions)
    st.session_state.current_q = 0
    st.session_state.answers = []
    st.success("Questions generated!")

# --- Main Flow ---
if "questions" in st.session_state:

    questions = st.session_state.questions
    current = st.session_state.current_q

    if current < len(questions):
        st.subheader(f"Q{current+1}: {questions[current]}")

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):
            if answer.strip() == "":
                st.warning("Please write an answer.")
            else:
                evaluation = evaluate_answer(questions[current], answer)
                st.session_state.answers.append(
                    {"question": questions[current], "answer": answer, "evaluation": evaluation}
                )
                st.session_state.current_q += 1
                st.rerun()
    else:
        st.header("🎉 Interview Completed")
        st.write("Here are your results:")

        for i, item in enumerate(st.session_state.answers, 1):
            st.subheader(f"Q{i}: {item['question']}")
            st.write("**Your Answer:**")
            st.write(item["answer"])
            st.write("**Evaluation:**")
            st.write(item["evaluation"])
            st.markdown("---")

