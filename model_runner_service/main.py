from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse

app = FastAPI()

# ----------------------------
# Request / Response Schemas
# ----------------------------

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]

class ChatChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str = "stop"

class ChatCompletion(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: List[ChatChoice]
    model: str

# ----------------------------
# Endpoint
# ----------------------------

@app.post("/chat/completions")
async def chat_completions(request: ChatRequest):
    prompt = request.messages[-1].content if request.messages else ""
    reply = (f"Reply from {request.model}. This runner answers locally instead of calling a "
             f"hosted model, so the text is canned. Your prompt was: {prompt}")

    response = ChatCompletion(
        id="local-model-runner-1",
        model=request.model,
        choices=[
            ChatChoice(
                index=0,
                message=Message(role="assistant", content=reply)
            )
        ]
    )

    return JSONResponse(content=response.dict())
