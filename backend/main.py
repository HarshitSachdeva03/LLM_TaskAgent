from fastapi import FastAPI, Request
from pydantic import BaseModel
from backend.agent.agent_core import run_agent_on_command

app = FastAPI()

class CommandRequest(BaseModel):
    command: str

@app.post("/api/agent")
async def run_agent_endpoint(request: CommandRequest):
    result = run_agent_on_command(request.command)
    return {"result": result}

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