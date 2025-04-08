from dataclasses import dataclass
import json
from typing import Any, Callable

from ollama import Client, Message

ToolRepository = dict[str, Callable]
Tools = dict[Callable, list[Any]]

@dataclass
class Toolkit:
    repository: ToolRepository
    handlers: Callable[[Message.ToolCall], Tools]

def agentic_chat(
    *,
    ollama_client: Client,
    llm: str,
    history: list[Message],
    toolkits: list[Toolkit],
) -> list[Message]:
    tool_repository: ToolRepository = {}
    for tool in toolkits:
        tool_repository = { **tool_repository, **tool.repository }

    def handlers(tool_call: Message.ToolCall) -> Tools:
        hs = {}
        for toolkit in toolkits:
            hs = { **hs, **toolkit.handlers(tool_call) }
        return hs

    chat = lambda tool_repository: ollama_client.chat(
        model=llm,
        messages=history,
        tools=None if tool_repository is None else [*tool_repository.values()],
    )
    message = chat(tool_repository).message
    tool_calls = [
        *filter(
            lambda tool_call: tool_call.function.name in tool_repository,
            message.tool_calls or []
        )
    ]

    new_history = [message]

    if len(tool_calls) == 0:
        new_history = [*new_history, chat(None).message]
        return new_history

    found_tool = False
    for tool_call in tool_calls:
        function_to_call: Callable | None = tool_repository.get(tool_call.function.name) # pyright: ignore
        if function_to_call is None:
            continue
        for [tool, args] in handlers(tool_call).items():
            if function_to_call.__name__ == tool.__name__:
                found_tool = True
                result = tool(*args)
                tool_message = Message(role="tool", content=json.dumps(result), tool_calls=[tool_call])
                new_history = [*new_history, tool_message]
                break

    if found_tool:
        new_history = [
            *new_history,
            ollama_client.chat(
                model=llm,
                messages=[*history, *new_history],
            ).message
        ]
    return new_history

def create_tool_repository(*functions: Callable) -> ToolRepository:
    return { function.__name__: function for function in functions }

def create_tool_handlers(factory: Callable[[Message.ToolCall], Tools]) -> Callable[[Message.ToolCall], Tools]:
    return lambda tool_call: factory(tool_call)
