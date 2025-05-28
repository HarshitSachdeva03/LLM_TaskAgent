import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env')) #since .env lies one directory above this llm_integration.py file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("GEMINI KEY:", os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def query_llm(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error using Gemini: {str(e)}"
