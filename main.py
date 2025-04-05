from fastapi import FastAPI, Request
from pydantic import BaseModel
from gpt_connector import GPTConnector

app = FastAPI()
gpt = GPTConnector()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    system_prompt = "أنت مساعد ذكي يساعد المستخدمين في الإجابة على استفساراتهم."
    reply = gpt.chat(user_id=request.user_id, user_input=request.message, system_prompt=system_prompt)
    return {"response": reply}


@app.post("/reset")
async def reset_chat(request: ChatRequest):
    gpt.reset(request.user_id)
    return {"message": "conversation reset"}