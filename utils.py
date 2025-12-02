# utils.py
import os
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found! Please set it in .streamlit/secrets.toml")

client = OpenAI(api_key=api_key)

import re
from typing import List

# initialize client (ensure OPENAI_API_KEY in env)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_llm(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 300) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.2
        )
        return response.choices[0].message["content"]
    except Exception as e:
        # Return a clear error string (Streamlit can show it)
        return f"LLM_ERROR: {str(e)}"

def _parse_numbered_or_bulleted_list(text: str) -> List[str]:
    """
    Try several strategies to extract a list of questions from the LLM text.
    Returns list of cleaned question strings (non-empty).
    """
    if not text:
        return []

    lines = text.splitlines()
    items = []

    # Strategy 1: capture lines that start with "1.", "1)", "1 -", "- ", "* "
    numbered_pattern = re.compile(r'^\s*(?:\d+[\.\)]|\-|\*|\•)\s*(.+)')
    for ln in lines:
        m = numbered_pattern.match(ln)
        if m:
            items.append(m.group(1).strip())

    # Strategy 2: if nothing found, split by blank lines and keep short blocks
    if not items:
        # try splitting by double newline
        blocks = [b.strip() for b in text.split('\n\n') if b.strip()]
        if len(blocks) > 1:
            items = blocks

    # Strategy 3: fallback — split by newline and keep non-empty lines
    if not items:
        items = [ln.strip() for ln in lines if ln.strip()]

    # Final cleanup: remove numbering at start if still present, remove trailing punctuation
    cleaned = []
    for it in items:
        # remove any leading numbering leftover like "1. " or "1) "
        it = re.sub(r'^\s*\d+[\.\)]\s*', '', it).strip()
        if it:
            cleaned.append(it)

    return cleaned

def generate_questions(role: str, skill: str, n: int = 5) -> List[str]:
    """
    Returns a list of questions (strings). Uses the LLM to generate questions,
    then parses the LLM output into a Python list robustly.
    """
    prompt = f"""
You are an interview question generator.

Produce exactly {n} interview questions for the role "{role}" focused on the skill "{skill}".
Return the questions as a numbered list (1. ...), but it's fine if output uses bullets.
Keep each question to one or two sentences.
"""
    raw = call_llm(prompt, max_tokens=400)

    # If the LLM returned an error string, forward it as single-item list so UI can show the message
    if raw.startswith("LLM_ERROR:"):
        return [raw]

    parsed = _parse_numbered_or_bulleted_list(raw)

    # If parser returned more items than requested, trim to n; if fewer, accept whatever we have
    if len(parsed) > n:
        parsed = parsed[:n]

    # If parser returned nothing, return the raw text as one item (so user sees what happened)
    if not parsed:
        return [raw.strip()]

    return parsed

def evaluate_answer(question: str, answer: str) -> str:
    """
    Returns the LLM's textual evaluation (you can extend to JSON parsing later).
    """
    prompt = f"""
You are an interviewer evaluator. Given a question and an answer, provide:
- A numeric score 1-10
- 2 short strengths
- 2 short weaknesses
- A one-line improvement suggestion

Return as plain text (not JSON).
Question 1:How do you approach designing a RESTful API?
Answer:You would design it using standard conventions like clear, resource-based URLs, appropriate HTTP methods (GET, POST, PUT, DELETE), and standard response codes. You would also consider aspects like versioning, request/response formats (like JSON), and authentication/authorization. 
"""
    return call_llm(prompt, max_tokens=400)
