#  Interview Bot 🤖
https://genai-interview-bot-6gyeadyseqvxzga6ymfmbz.streamlit.app/

Video link :- https://drive.google.com/file/d/1asBsLCnQ7iHszyAzVgbPx8TSpZ9s4GMg/view?usp=sharing

A minimal AI-powered interview bot that:
- Generates interview questions by role & skill
- Collects candidate answers
- Evaluates answers using an LLM rubric (fluency, correctness, completeness, examples)
- Saves transcripts
- Runs via CLI or Streamlit UI

## Run (CLI)

```
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
python interview_bot.py
```

## Run (Streamlit)

```
streamlit run streamlit_app.py
```

## Features
- Question generation
- Structured evaluation JSON
- Transcript saving
- Easy to extend
