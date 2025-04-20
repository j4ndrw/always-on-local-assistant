from ollama import Message

from src.agent.tools.tools import define_toolkit, description

from ....settings.settings import settings
from ...client import ollama_client
from ...models.conversation import history
from ...utils.prompt import SYSTEM_PROMPT

tool, resource, register_toolkit = define_toolkit()


@tool.create(
    description=description(
        """
        Forgets the conversation with the user.
        NOTE: Only use this tool if the user **explicitely** asks for the conversation to be erased or forgotten.
        """,
        returns=[("dict", "A JSON object, containing an error or a success status")],
    ),
)
def forget_conversation() -> dict:
    global history
    history = [SYSTEM_PROMPT]

    return tool.success(forget_conversation.__name__)


@tool.create(
    description=description(
        """
        Delegates a task to a different language model, designed to solve complex reasoning tasks.
        For example, if the user asks for a logic puzzle to be solved, the reasoning language model
        will be asked to provide the solution.

        NOTE: You will have to rephrase the task in such a way that it is clear for
        the reasoning model what needs to be done!
        """,
        args=[
            (
                "task",
                'The task at hand. E.g. "If I have 5 apples and Jimmy takes 2, how many apples do I have left?"',
            )
        ],
        returns=[
            ("str | dict", "The string response from the reasoning model or an error.")
        ],
    ),
)
def delegate_task_to_reasoning_model(task: str) -> str | dict:
    if not task:
        return tool.error(
            delegate_task_to_reasoning_model.__name__,
            error="No task provided to reasoning model.",
        )

    try:
        content = ollama_client.chat(
            model=settings.reasoning_llm,
            messages=[Message(role="assistant", content=task)],
        ).message.content
        if not content:
            return tool.error(
                delegate_task_to_reasoning_model.__name__,
                error="Reasoning model didn't respond with anything.",
            )
        return content
    except Exception as e:
        print(e)
        return tool.error(
            delegate_task_to_reasoning_model.__name__,
            error=f"Reasoning model request failed.",
        )
