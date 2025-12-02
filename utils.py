# utils.py
import os
from typing import List, Dict
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt, model="gpt-4o-mini", max_tokens=300):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role":"user", "content": prompt}],
        temperature=0.2,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def generate_questions(role: str, skill: str, n=5) -> List[str]:
    prompt = f"""Generate {n} interview questions for role '{role}' focused on skill '{skill}'.
Return a numbered list with difficulty (easy/medium/hard)."""
    out = call_llm(prompt)
    return out.strip().splitlines()

def evaluate_answer(question: str, answer: str) -> Dict:
    prompt = f"""
Evaluate the candidate's answer in JSON format.

Question: {question}
Answer: {answer}

Return JSON:
{{
  "scores": {{
      "fluency": 0-5,
      "correctness": 0-5,
      "completeness": 0-5,
      "examples": 0-5
  }},
  "overall": 0-100,
  "feedback": "short paragraph"
}}
"""
    out = call_llm(prompt, max_tokens=400)
    try:
        return json.loads(out)
    except:
        return {"raw": out}
