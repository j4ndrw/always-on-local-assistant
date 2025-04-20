import json

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from ollama import Message

from .src.agent.agent import agentic_chat
from .src.agent.frontend_capabilities import frontend_capabilities_toolkit
from .src.agent.conversation import Conversation, history
from .src.agent.to_do_list import to_do_toolkit
from .src.agent.weather import weather_toolkit
from .src.agent.conversation import conversation_toolkit
from .src.settings.settings import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/conversation")
async def conversation(conversation: Conversation, request: Request):
    if request.headers.get("x-secret") != settings.secret:
        return Response(status_code=403)

    settings.metadata = conversation.metadata
    ephemeral_history: list[Message] = []

    print(f"USER: {conversation.prompt}")

    user_message = Message(role="user", content=conversation.prompt)
    history.append(user_message)
    ephemeral_history.append(user_message)

    agent_messages = agentic_chat(
        llm=settings.llm,
        history=history,
        toolkits=[
            to_do_toolkit,
            frontend_capabilities_toolkit,
            weather_toolkit,
            conversation_toolkit # experimental - might delete if impractical
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
