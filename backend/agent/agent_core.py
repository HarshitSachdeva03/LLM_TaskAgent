# agent/agent_core.py

import json
import re
from backend.agent.tools import send_email, create_calendar_event
from backend.agent.llm_integration import query_llm
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

def run_agent_on_command(user_input: str, history: list[str]) -> tuple[str, list[str]]:
    today_str = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""You are a helpful assistant that only helps users with two actions:
1. Sending emails
2. Creating calendar events

Today is {today_str}.
Your job is to understand the conversation and do one of the following:
- If the user input is unclear or missing important details, respond with a clarifying question
- If the input is unrelated to email/calendar, politely say you can only help with those
- If you're ready to perform the action, return a valid JSON object in exactly one of the following formats:

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
  "start": "2025-05-28 17:00"
}}

3. For clarification:
{{
  "action": "clarify",
  "question": "What time should I set the reminder for?"
}}

4. For rejection:
{{
  "action": "reject",
  "message": "Sorry, I can only help with emails and calendar events."
}}

Conversation so far:
{''.join(history)}

User: {user_input}
Assistant:"""

    response = query_llm(prompt)
    history.append(f"User: {user_input}\nAssistant: {response}\n")

    data = extract_json_from_text(response)
    if not data:
        return f"❌ Couldn't parse LLM response:\n\n{response}", history

    action = data.get("action")

    if action == "email":
        result = send_email(data["recipient"], data["subject"], data["body"])
        return f"✅ {result}", history

    elif action == "calendar":
        result = create_calendar_event(data["title"], data["start"])
        return f"📅 {result}", history

    elif action == "clarify":
        return data.get("question", "Can you clarify your request?"), history

    elif action == "reject":
        return data.get("message", "I'm limited to emails and calendar events."), history

    else:
        return f"❌ Unrecognized action: {action}\n\n{response}", history
