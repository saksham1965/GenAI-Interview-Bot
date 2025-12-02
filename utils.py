# utils.py
import os
from openai import OpenAI

# Load API key from environment variable
API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def call_llm(prompt, model="gpt-4o-mini", temperature=0.7, max_tokens=300):
    """
    Helper function to call OpenAI chat completion
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM_ERROR: {e}"


def generate_questions(role, skill, n=5):
    """
    Generate interview questions based on role & skill
    """
    prompt = f"""
    Generate {n} interview questions for a candidate applying for the role: {role}
    focused on the skill: {skill}.
    Return only a numbered list.
    """

    output = call_llm(prompt)

    if output.startswith("LLM_ERROR"):
        return [output]

    return output.split("\n")


def evaluate_answer(question, answer):
    """
    Evaluate candidate's answer with a scoring rubric.
    """
    prompt = f"""
    Evaluate the following answer to an interview question.

    Question: {question}
    Candidate Answer: {answer}

    Give:
    - Score (1–10)
    - Strengths
    - Weaknesses
    - Final feedback summary
    """

    return call_llm(prompt)
