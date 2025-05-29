from fastapi import FastAPI, Request
from pydantic import BaseModel
from backend.agent.agent_core import run_agent_on_command
from typing import List

app = FastAPI()

class CommandRequest(BaseModel):
    command: str

class ChatRequest(BaseModel):
    message: str
    history: List[str]

@app.post("/api/agent")
async def run_agent_endpoint(request: CommandRequest):
    result,_ = run_agent_on_command(request.command,[])
    return {"result": result}

@app.post("/api/chat")
async def chat_agent(request: ChatRequest):
    response, updated_history = run_agent_on_command(request.message, request.history)
    return {"reply": response, "history": updated_history}

@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM Agent API. Visit /docs to test."}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)