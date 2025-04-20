import sys

from ollama import Message
from pprint import pprint

from src.agent.agent import agentic_chat
from src.agent.conversation import Conversation, history
from src.settings.settings import settings

from src.agent.frontend_capabilities import frontend_capabilities_toolkit
from src.agent.to_do_list import to_do_toolkit
from src.agent.weather import weather_toolkit
from src.agent.conversation import conversation_toolkit
from src.settings.settings import settings

metadata = {
    "contacts": {
        "John Doe": "+99012345678"
    },
    "installedApps": ["com.whatsapp", "com.google.android.youtube"],
    "gpsPosition": {
        "latitude": 12.34,
        "longitude": 34.56,
    }
}

if __name__ == "__main__":
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
        print(f"[LOLA]: {answer.content}")

        used_tools = [*set(tool_call.function.name for message in ephemeral_history for tool_call in message.tool_calls or [])]
        if len(used_tools) > 0:
            print(f"[TOOLS USED FOR RESPONSE]: {', '.join(used_tools)}")

        print("\n------------------------\n")
