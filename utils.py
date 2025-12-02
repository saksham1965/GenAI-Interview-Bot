import os
from typing import List, Dict

API_KEY = os.getenv("OPENAI_API_KEY")
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_llm(prompt: str, model="gpt-4o-mini", max_tokens=300):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.2
    )
    return response.choices[0].message.content


def generate_questions(role: str, skill: str, n=5) -> List[str]:
    prompt = f"""You are an interview question generator.
Produce {n} interview questions for role "{role}" focused on skill "{skill}".
Return numbered list and label each with difficulty: easy/medium/hard.
"""
    out = call_llm(prompt)
    return out.strip().splitlines()

def evaluate_answer(question: str, answer: str) -> Dict:
    rubric_prompt = f"""
You are an interview evaluator. Given a question and candidate answer, return a JSON with:
- scores: {{fluency:0-5, correctness:0-5, completeness:0-5, examples:0-5}}
- overall: 0-100 (integer)
- feedback: one short paragraph with specific improvement points.

Question: {question}
Answer: {answer}

Return only valid JSON.
"""
    out = call_llm(rubric_prompt, max_tokens=400)
    import json
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out}
