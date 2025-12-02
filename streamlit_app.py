import streamlit as st
import os
import json 

# Load secret into environment
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

from utils import generate_questions, evaluate_answer

st.title("AI Interview Bot — Demo")

role = st.text_input("Role", "Backend Engineer")
skill = st.text_input("Skill", "APIs")

if st.button("Generate Questions"):
    qs = generate_questions(role, skill, n=5)
    st.session_state["questions"] = qs

if "questions" in st.session_state:
    for i,q in enumerate(st.session_state["questions"],1):
        st.subheader(f"Q{i}")
        st.write(q)
        ans = st.text_area(f"Your answer to Q{i}", key=f"a{i}")
        if st.button(f"Evaluate Q{i}", key=f"eval{i}"):
            res = evaluate_answer(q, ans)
            st.write(res)
            os.makedirs("sample_transcripts", exist_ok=True)
            fname = f"sample_transcripts/{role.replace(' ','_')}_{skill}_{i}.json"
            with open(fname,"w") as f:
                json.dump({"q":q,"a":ans,"eval":res}, f, indent=2)
            st.success(f"Saved transcript to {fname}")
