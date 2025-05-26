import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google.auth.transport.requests import Request

load_dotenv()

# Scopes for Gmail and Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.events'
]

def get_google_creds():
    creds = None
    token_file = 'creds/token.json'

    # Load existing token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If no valid credentials, go through OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("GOOGLE_CLIENT_SECRET_FILE"), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save token
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds

def send_email(to, subject, message_text):
    creds = get_google_creds()
    service = build('gmail', 'v1', credentials=creds)

    message = {
        'raw': create_raw_email(to, subject, message_text)
    }

    send_message = service.users().messages().send(userId='me', body=message).execute()
    return f"Email sent to {to}, ID: {send_message['id']}"

def create_raw_email(to, subject, message_text):
    import base64
    from email.mime.text import MIMEText

    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return raw

def create_calendar_event(summary, start_time_str, duration_minutes=60):
    creds = get_google_creds()
    service = build('calendar', 'v3', credentials=creds)

    start_time = datetime.datetime.fromisoformat(start_time_str)
    end_time = start_time + datetime.timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return f"Event created: {event_result['htmlLink']}"
