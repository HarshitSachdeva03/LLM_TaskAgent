# 🤖 AI-Powered Workflow Assistant

A full-stack conversational agent powered by Gemini LLM that can send emails and schedule calendar events via Gmail and Google Calendar. Interact through a chat-like interface with follow-up questions, clarifications, and natural dialogue flow.

---

## 🔍 Features

- 💬 **Conversational Chat**: Multi-turn chat UI that asks clarifying questions before taking actions.
- ✉️ **Email & Calendar Actions**: Send emails and create events based on natural language commands.
- 🧠 **Gemini LLM Integration**: Prompt-engineered to output structured JSON for accurate tool execution.
- 🧱 **Session Context**: Maintains chat history to support context-aware interactions.
- 🎨 **Modern UI**: React + Vite chat interface with styled message bubbles and responsive layout.
- ⚙️ **Developer Setup**: Includes CORS support, environment loading, and modular code structure.

---

## 🚀 Project Structure

```

ai\_workflow\_agent/
├── backend/
│   ├── agent/
│   │   ├── agent\_core.py       # LLM logic + chat + tool routing
│   │   ├── tools.py            # Gmail & Calendar wrapper functions
│   │   └── llm\_integration.py  # Gemini API & .env loader
│   ├── main.py                 # FastAPI server with /api/chat
│   ├── requirements.txt
│   └── .env                    # API keys & config flags
└── llm-ui/
├── src/
│   └── App.jsx             # Chat UI frontend
└── package.json

````

---

## ⚙️ Prerequisites

- Python 3.10+
- Node.js v16+ and npm (or yarn)
- Google OAuth credentials (`credentials.json`)
- Gemini API key from Google

---

## 🧭 Setup & Run Guide

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USER/ai_workflow_agent.git
cd ai_workflow_agent
````

---

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file with:

```env
GOOGLE_CLIENT_SECRET_FILE=creds/credentials.json
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MOCK=false
```

Add your Google OAuth credentials into:

```
backend/creds/credentials.json
```

---

### 3. Run the Backend Server

```bash
uvicorn backend.main:app --reload --port 8000
```

#### Available endpoints:

* `GET /` – Health check
* `POST /api/chat` – Chat interaction (JSON: `{ message, history }`)

---

### 4. Frontend Setup

```bash
cd ../llm-ui
npm install
npm run dev
```

Visit: `http://localhost:5173`

---

## 🗣️ How to Use

1. Start both backend and frontend services.
2. In the chat interface, type commands like:

   ```
   Set a reminder for project meeting at 5 pm.
   ```
3. The assistant may ask:

   ```
   Sure — what's the meeting title?
   ```
4. Reply with the title.
5. It’ll confirm when the event is created.

---

## ⚙️ Configuration Options

* **Fallback/Mock Mode**: Set `LLM_MOCK=true` in `.env` to test behavior without a Gemini key.
* **Tool Extensions**: Add more functions in `tools.py`, then update prompt logic in `agent_core.py`.
* **UI Customization**: Modify `App.jsx` to change styling, add timestamps, or features.

---

## 🛠️ Troubleshooting

* **CORS Errors**: Ensure `CORSMiddleware` is enabled in `main.py`.
* **Auth Issues**: If Gmail/Calendar access fails, delete `token.json` and re-authenticate.
* **LLM Problems**: Missing or invalid Gemini key? Check `.env` and restart backend.

---

## ✅ Next Steps (Optional Enhancements)

* Add support for attachments or multiple recipients
* Integrate Model Context Protocol (MCP) for tool access standardization
* Be creative and extend its functionality !

---

Built with Gemini LLM, FastAPI, React, and Vite.

---

⭐ If you found this assistant useful, please give it a star and share feedback!

