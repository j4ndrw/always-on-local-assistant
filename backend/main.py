import json
from typing import Any, Callable, Iterator

import ollama
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from ollama import ChatResponse, Message
from pydantic import BaseModel

from .src.agent.agent import agentic_chat
from .src.agent.frontend_capabilities import frontend_capabilities_toolkit
from .src.agent.to_do_list import to_do_toolkit
from .src.agent.weather import weather_toolkit

from .src.settings.settings import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ollama_client = ollama.Client("http://localhost:7869")
history: list[Message] = [
    Message(role="system", content="""
        You are Lola, an voice-based AI agent, capable of answering questions, as well as performing tasks, provided you have the necessary tools.

        Note that you are also capable of opening applications on the user's device, and interact with the device in various other ways.
        Please do not default to refusing prompts related to interacting the the user's device.

        Only answer in plain text instead of markdown, because your answer will be passed through a text-to-speech model.
    """)
]

def stream_conversation(stream: Iterator[ChatResponse], *, on_done: Callable[[Message], None] | None = None):
    answer: Message | None = None
    for chunk in stream:
        answer = chunk.message
        yield chunk.message.content
    if answer is not None and on_done is not None:
        on_done(answer)

class Conversation(BaseModel):
    prompt: str
    metadata: dict[str, Any]

@app.post("/api/conversation")
async def conversation(conversation: Conversation, request: Request):
    if request.headers.get("x-secret") != settings.secret:
        return Response(status_code=403)

    print(f"USER: {conversation.prompt}")

    ephemeral_history: list[Message] = []

    settings.metadata = conversation.metadata

    user_message = Message(role="user", content=conversation.prompt)
    history.append(user_message)
    ephemeral_history.append(user_message)

    agent_messages = agentic_chat(
        ollama_client=ollama_client,
        llm=settings.llm,
        history=history,
        toolkits=[
            to_do_toolkit,
            frontend_capabilities_toolkit,
            weather_toolkit
        ]
    )
    history.extend(agent_messages)
    ephemeral_history.extend(agent_messages)

    answer = history[-1]
    print(f"LOLA: {answer.content}")

    return Response(
        json.dumps([{ "role": message.role, "content": message.content } for message in ephemeral_history]),
        media_type="text/plain"
    )
