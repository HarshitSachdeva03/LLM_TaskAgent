# AI Workflow Agent

A tool that integrates with Google services to manage emails and calendar events.

## Features
- Send emails via Gmail API
- Create calendar events via Google Calendar API

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up Google API credentials
3. Create a `.env` file with your Google client secret file path

.env file contains the following:
    GOOGLE_CLIENT_SECRET_FILE=creds/credentials.json
    GEMINI_API_KEY="Your key here"

creds/ contains:
    -credentials.json: obtained from google (OAuth client secret)
    -token.json: generated after the user authorizes login

## ⚙️ Key Technologies & Libraries

| Component        | Library / Tool                                        | Purpose                                           |
| ---------------- | ----------------------------------------------------- | ------------------------------------------------- |
| **LLM**          | `google.generativeai`                                 | Interact with Gemini LLM via prompt engineering   |
| **Email API**    | `google-api-python-client`, `oauthlib`, `google-auth` | Send Gmail messages                               |
| **Calendar API** | Same as above                                         | Schedule events on user's Google Calendar         |
| **Environment**  | `python-dotenv`                                       | Securely load `.env` variables                    |
| **Time Parsing** | `python-dateutil`                                     | Robustly interpret human-like time strings        |
| **OAuth Flow**   | `InstalledAppFlow`                                    | Authenticates access to user's Gmail and Calendar |
| **Language**     | Python 3                                              | Full stack logic for agent orchestration          |

---

## 🧠 How It Works (Step-by-Step)

1. **Natural Language Input**
   User enters a natural command like:

   > *"Send an email to Alice saying the meeting is postponed"*
   > or
   > *"Add a calendar event at 6pm tomorrow titled Project Review"*

2. **LLM Processing (Gemini)**
   The prompt is passed to **Gemini-2.0 Flash** using:
python
   model.generate_content(prompt)
   
The LLM replies with **structured JSON** indicating the type of task and parameters:
json
   {
     "action": "email",
     "recipient": "alice@example.com",
     "subject": "Meeting Postponed",
     "body": "The meeting has been postponed."
   }
   
3. **Parsing & Decision Logic**
   The agent extracts this JSON and determines whether the action is:

   * Sending an email → Calls `send_email()` in `tools.py`
   * Creating a calendar event → Calls `add_calendar_event()`

4. **Google API Actions**
   The chosen method uses authenticated Google APIs:

   * `gmail.users().messages().send(...)`
   * `calendar.events().insert(...)`

5. **OAuth & Tokens**
   If the user hasn't authorized the app yet, a browser-based flow is triggered. The generated access token is saved in `creds/token.json`.

---