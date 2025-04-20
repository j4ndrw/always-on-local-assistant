from pprint import pprint

from ollama import Message

from src.agent.agent import agentic_chat
from src.agent.models.conversation import Conversation, history
from src.agent.tools.tools import toolkits
from src.settings.settings import settings

metadata = {
    "contacts": {"John Doe": "+99012345678"},
    "installedApps": ["com.whatsapp", "com.google.android.youtube"],
    "gpsPosition": {
        "latitude": 12.34,
        "longitude": 34.56,
    },
}


def run_prompter():
    while True:
        prompt = input("[USER]: ")
        conversation = Conversation(prompt=f"lola {prompt}", metadata=metadata)
        settings.metadata = conversation.metadata
        ephemeral_history: list[Message] = []

        user_message = Message(role="user", content=conversation.prompt)
        history.append(user_message)
        ephemeral_history.append(user_message)

        agent_messages = agentic_chat(
            llm=settings.llm,
            history=history,
        )
        history.extend(agent_messages)
        ephemeral_history.extend(agent_messages)

        answer = history[-1]
        print(f"[LOLA]: {answer.content}")

        used_tools = [
            *set(
                tool_call.function.name
                for message in ephemeral_history
                for tool_call in message.tool_calls or []
            )
        ]
        if len(used_tools) > 0:
            print(f"[TOOLS USED FOR RESPONSE]: {', '.join(used_tools)}")

        print("\n------------------------\n")


if __name__ == "__main__":
    run_prompter()
