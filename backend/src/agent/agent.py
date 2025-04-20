import json
from typing import Callable

from ollama import Message

from .client import ollama_client
from .tools.tools import ToolHandlers, ToolRepository, load_toolkits


def agentic_chat(
    *,
    llm: str,
    history: list[Message],
    toolkits_path: str = "./src/agent/tools/toolkits"
) -> list[Message]:
    toolkits = load_toolkits(toolkits_path)
    history_snapshot = [*history]

    tool_repository: ToolRepository = {}
    tool_handlers: ToolHandlers = {}
    for tool in toolkits:
        tool_repository = {**tool_repository, **tool.repository}
        tool_handlers = {**tool_handlers, **tool.handlers}

    chat = lambda tool_repository: ollama_client.chat(
        model=llm,
        messages=history_snapshot,
        tools=None if tool_repository is None else [*tool_repository.values()],
    )
    message = chat(tool_repository).message
    tool_calls = [
        *filter(
            lambda tool_call: tool_call.function.name in tool_repository,
            message.tool_calls or [],
        )
    ]

    new_history = [message]

    if len(tool_calls) == 0:
        new_history = [*new_history, chat(None).message]
        return new_history

    found_tool = False
    for tool_call in tool_calls:
        function_to_call: Callable | None = tool_repository.get(
            tool_call.function.name
        )  # pyright: ignore
        if function_to_call is None:
            continue
        for [tool, args] in tool_handlers.items():
            if function_to_call.__name__ == tool.__name__:
                found_tool = True
                result = tool(*args(tool_call))
                tool_message = Message(
                    role="tool", content=json.dumps(result), tool_calls=[tool_call]
                )
                new_history = [*new_history, tool_message]
                break

    if found_tool:
        new_history = [
            *new_history,
            ollama_client.chat(
                model=llm,
                messages=[*history_snapshot, *new_history],
            ).message,
        ]
    return new_history
