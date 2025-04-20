from typing import Any
from ollama import Message
from pydantic import BaseModel

from ..settings.settings import settings
from .client import ollama_client
from .agent import Toolkit, create_tool_handlers, create_tool_repository
from .prompt import SYSTEM_PROMPT
from .error import agent_tool_error
from .success import agent_tool_success

history: list[Message] = [SYSTEM_PROMPT]

class Conversation(BaseModel):
    prompt: str
    metadata: dict[str, Any]

def forget_conversation() -> dict:
    """
    Forgets the conversation with the user.
    NOTE: Only use this tool if the user **explicitely** asks for the conversation to be erased or forgotten.

    Returns:
        dict: A JSON object, containing an error or a success status
    """
    global history
    history = [SYSTEM_PROMPT]

    return agent_tool_success(forget_conversation.__name__)

def delegate_task_to_reasoning_model(task: str) -> str | dict:
    """
    Delegates a task to a different language model, designed to solve complex reasoning tasks.
    For example, if the user asks for a logic puzzle to be solved, the reasoning language model
    will be asked to provide the solution.

    NOTE: You will have to rephrase the task in such a way that it is clear for
    the reasoning model what needs to be done!

    Args:
        task: The task at hand. E.g. "If I have 5 apples and Jimmy takes 2, how many apples do I have left?"

    Returns:
        str | dict: The string response from the reasoning model or an error.
    """
    if not task:
        return agent_tool_error(delegate_task_to_reasoning_model.__name__, message="No task provided to reasoning model.")

    try:
        content = ollama_client.chat(
            model=settings.reasoning_llm,
            messages=[Message(role="assistant", content=task)],
        ).message.content
        if not content:
            return agent_tool_error(delegate_task_to_reasoning_model.__name__, message="Reasoning model didn't respond with anything.")
        return content
    except Exception as e:
        print(e)
        return agent_tool_error(delegate_task_to_reasoning_model.__name__, message=f"Reasoning model request failed.")

_repository = create_tool_repository(
    forget_conversation,
    delegate_task_to_reasoning_model
)
_handlers = create_tool_handlers(lambda tool_call: {
    forget_conversation: [],
    delegate_task_to_reasoning_model: [tool_call.function.arguments.get('task')]
})

conversation_toolkit = Toolkit(repository=_repository, handlers=_handlers)
