from typing import Any

from ollama import Message
from pydantic import BaseModel

from ..utils.prompt import SYSTEM_PROMPT


class Conversation(BaseModel):
    prompt: str
    metadata: dict[str, Any]


history: list[Message] = [SYSTEM_PROMPT]
