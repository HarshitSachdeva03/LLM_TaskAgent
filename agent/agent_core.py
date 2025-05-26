# agent/agent_core.py

import json
import re
from agent.tools import send_email, create_calendar_event
from agent.llm_integration import query_llm
from datetime import datetime

def extract_json_from_text(text: str) -> dict | None:
    """
    Find the first JSON object in the given text and parse it.
    Returns a dict or None if parsing fails.
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None

def run_agent():
    print("🤖 Welcome to your Workflow AI Agent (Gemini powered)\n")

    while True:
        command = input("📝 What would you like me to do? (or type 'exit'): ")
        if command.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        today_str = datetime.now().strftime("%Y-%m-%d")
        prompt = f"""You're an AI assistant. Today is {today_str}. Based on this user command:
"{command}", decide if the user wants to send an email or create a calendar event.

Return exactly one JSON object, and nothing else, in one of these formats:

1. For email:
{{
  "action": "email",
  "recipient": "example@gmail.com",
  "subject": "Subject line",
  "body": "Email content"
}}

2. For calendar:
{{
  "action": "calendar",
  "title": "Meeting title",
  "start": "2025-04-22 14:00"
}}
Make sure the 'start' time is computed based on today ({today_str}) if the user says 'today'.
Do NOT wrap the JSON in backticks or add any explanation—just output the raw JSON."""
        response = query_llm(prompt)

        data = extract_json_from_text(response)
        if not data:
            print("⚠️ Couldn't parse response:", response)
            continue

        action = data.get("action")
        if action == "email":
            result = send_email(
                data["recipient"],
                data["subject"],
                data["body"]
            )
            print("✅", result)

        elif action == "calendar":
            result = create_calendar_event(
                data["title"],
                data["start"]
            )
            print("📅", result)

        else:
            print("❌ Unrecognized action type in JSON:", action)
