# streamlit_app.py
import streamlit as st
import os
from utils import generate_questions, evaluate_answer

st.set_page_config(page_title="AI Interview Bot", layout="centered")

st.title("AI Interview Bot — Demo")

# Optional: load secret into env (if using Streamlit Cloud)
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

role = st.text_input("Role", "Backend Engineer")
skill = st.text_input("Skill", "APIs")
n_questions = st.number_input("Number of questions", min_value=1, max_value=10, value=5)

if st.button("Generate Questions"):
    with st.spinner("Generating questions..."):
        qs = generate_questions(role, skill, n=int(n_questions))
    # qs is expected to be a list; handle fallback
    if isinstance(qs, list):
        st.session_state["questions"] = qs
        st.success(f"Generated {len(qs)} items")
        # show debug raw content if parser might have failed (single long item)
        if len(qs) == 1 and len(qs[0].splitlines()) > 3:
            st.info("LLM returned a single block — displaying raw text. If this looks odd, try changing the model or prompt.")
            st.text(qs[0])
    else:
        # just in case something not list is returned
        st.session_state["questions"] = [str(qs)]
        st.warning("Unexpected response format from generate_questions; showing raw response.")

if "questions" in st.session_state:
    st.header("Questions")
    for i, q in enumerate(st.session_state["questions"], start=1):
        st.subheader(f"Q{i}")
        st.write(q)
        ans_key = f"answer_{i}"
        st.text_area(f"Your answer to Q{i}", key=ans_key, height=120)
        if st.button(f"Evaluate Q{i}", key=f"eval_{i}"):
            answer = st.session_state.get(ans_key, "").strip()
            if not answer:
                st.warning("Please type/paste an answer before evaluation.")
            else:
                with st.spinner("Evaluating..."):
                    eval_text = evaluate_answer(q, answer)
                st.markdown("**Evaluation result:**")
                st.text(eval_text)
                # save transcript
                import json, time
                os.makedirs("sample_transcripts", exist_ok=True)
                fname = f"sample_transcripts/{role.replace(' ','_')}_{skill}_{int(time.time())}_q{i}.json"
                with open(fname, "w") as f:
                    json.dump({"q": q, "a": answer, "eval": eval_text}, f, indent=2)
                st.success(f"Saved transcript to {fname}")

# show small footer and debug
st.write("---")
if st.button("Show debug env"):
    st.write("OPENAI_API_KEY present in env:", bool(os.environ.get("OPENAI_API_KEY")))
