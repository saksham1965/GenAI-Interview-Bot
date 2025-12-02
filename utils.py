# utils.py
import os
from openai import OpenAI

# Load OpenAI client (key must be in environment)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# -----------------------------
# Call LLM
# -----------------------------
def call_llm(prompt, model="gpt-4o-mini", max_tokens=300):
    """
    Sends a prompt to OpenAI Chat Completion API.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ LLM Error: {str(e)}"


# -----------------------------
# Question Generator
# -----------------------------
def generate_questions(role, skill, n=5):
    prompt = f"""
    Generate {n} interview questions for the following:

    Role: {role}
    Skill Focus: {skill}

    Give questions only, numbered 1 to {n}.
    """
    return call_llm(prompt)


# -----------------------------
# Answer Evaluation
# -----------------------------
def evaluate_answer(question, answer):
    prompt = f"""
    Evaluate the following interview answer.

    Question: {question}
    Candidate Answer: {answer}

    Provide:
    - Score (1–10)
    - Strengths
    - Weaknesses
    - Final short feedback
    """
    return call_llm(prompt, max_tokens=400)
