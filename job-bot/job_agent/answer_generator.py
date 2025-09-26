import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

with open("resume.json", "r", encoding="utf-8") as f:
    RESUME_JSON = json.load(f)

RESUME_TEXT = json.dumps(RESUME_JSON)

def generate_answer(question):
    for key, ans in CONFIG["custom_answers"].items():
        if key.lower() in question.lower():
            return ans
    prompt = f"""
Resume:
{RESUME_TEXT}

Question: {question}
Provide a short, professional answer based on the resume.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except:
        return "I am highly motivated and eager to contribute."
