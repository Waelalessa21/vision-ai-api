from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gpt_connector import GPTConnector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gpt = GPTConnector()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    with open("chat_template.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()
    
    reply = gpt.chat(user_id=request.user_id, user_input=request.message, system_prompt=system_prompt)
    return {"response": reply}


@app.post("/reset")
async def reset_chat(request: ChatRequest):
    gpt.reset(request.user_id)
    return {"message": "conversation restting"}


@app.get("/")
async def root():
    return {"message": "Vision AI API is running"}