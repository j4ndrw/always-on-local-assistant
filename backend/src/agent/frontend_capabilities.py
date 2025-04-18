import urllib.parse
from dataclasses import asdict, dataclass, field
from typing import Any

from ..settings.settings import settings
from ..utils import find_similar
from .agent import Toolkit, create_tool_handlers, create_tool_repository
from .error import agent_tool_error

Todos = dict[str, bool]
todos: Todos = {}


@dataclass
class FrontendCapability:
    kind: str
    data: dict[str, Any]
    archetype: str = field(default_factory=lambda: "frontend-capability")

    def dict(self):
        return {k: v for k, v in asdict(self).items()}

def frontend_capability(*, kind: str, data: dict[str, Any]) -> dict:
    return FrontendCapability(kind=kind, data=data).dict()

def open_application(application_name: str) -> dict:
    """
    Opens the application on the user's phone (e.g. YouTube, Whatsapp, etc...)
    NOTE: Only use this tool if the user **explicitely** asks for an app to be opened.

    Args:
        application_name: The name of the application that needs to be opened (e.g. YouTube, Whatsapp, etc...)

    Returns:
        dict: A JSON object, containing the url of the application that needs to be opened
    """

    if not application_name:
        return agent_tool_error(open_application.__name__, message="No application name provided.")

    installed_apps: list[str] = settings.metadata.get("installedApps", [])
    if len(installed_apps) == 0:
        return agent_tool_error(open_application.__name__, message="No apps installed on the user's device")

    found_app, similarity = find_similar(installed_apps, application_name.lower(), lambda app: app.split(".")[-1].lower())
    if found_app is None or similarity is None:
        return agent_tool_error(open_application.__name__, message=f"No application similar to {application_name} was found.")

    if similarity <= 0.5:
        return agent_tool_error(open_application.__name__, message=f"{found_app} is not exactly similar to {application_name}. Aborting...")

    return frontend_capability(kind="open-app", data={"url": found_app})

def send_whatsapp_message(to: str, message: str) -> dict:
    """
    Sends a WhatsApp message to a contact.
    NOTE: Only use this tool if the user **explicitely** asks for a message to be sent to a contact.
    IMPORTANT: This tool only prepares the message to be sent. It is only sent if the user approves the action.

    Args:
        to: The name of the contact that the user wants to send a message to
        message: The message to send to the contact

    Returns:
        dict: A JSON object, containing the url of the WhatsApp application that needs to be opened with
              the appropriate parameters so that the message can be sent.
    """
    if not to:
        return agent_tool_error(send_whatsapp_message.__name__, message="No recipient provided.")

    if not message:
        return agent_tool_error(send_whatsapp_message.__name__, message="No message to send to recipient was provided.")

    installed_apps: list[str] = settings.metadata.get("installedApps", [])
    if len(installed_apps) == 0:
        return agent_tool_error(send_whatsapp_message.__name__, message="No applications installed on the user's device.")

    contacts_map: dict[str, str] = settings.metadata.get("contacts", {})
    if len(contacts_map.keys()) == 0:
        return agent_tool_error(send_whatsapp_message.__name__, message="No contacts found on the user's device")

    found_app, similarity = find_similar(installed_apps, "WhatsApp".lower(), lambda app: app.split(".")[-1].lower())
    if found_app is None or similarity is None or similarity <= 0.5:
        return agent_tool_error(send_whatsapp_message.__name__, message="No application similar to WhatsApp was found.")

    found_contact, similarity = find_similar(contacts_map.keys(), to.lower(), lambda contact: contact.lower())
    if found_contact is None or similarity is None or similarity <= 0.2:
        return agent_tool_error(send_whatsapp_message.__name__, message=f"No contact similar to {to} was found.")

    phone_number = contacts_map.get(found_contact, None)
    if phone_number is None:
        return agent_tool_error(send_whatsapp_message.__name__, message=f"Contact {found_contact} has no phone number associated to it.")

    return frontend_capability(
        kind="open-app-with-intent",
        data={
            "package": found_app,
            "url": f"https://api.whatsapp.com/send?phone={phone_number}&text={message}",
        }
    )

def search_on_youtube(search_query: str) -> dict:
    """
    Sends a WhatsApp message to a contact.
    NOTE: Only use this tool if the user **explicitely** asks for a message to be sent to a contact.
    IMPORTANT: This tool only prepares the message to be sent. It is only sent if the user approves the action.

    Args:
        search_query: The thing the user wants to search for on YouTube

    Returns:
        dict: A list of JSON object, containing the url of the
              YouTube application that needs to be opened with
              the appropriate parameters.
    """
    if not search_query:
        return agent_tool_error(search_on_youtube.__name__, message="No search query provided")

    installed_apps: list[str] = settings.metadata.get("installedApps", [])
    if len(installed_apps) == 0:
        return agent_tool_error(search_on_youtube.__name__, message="No applications installed on the user's device.")

    found_app, similarity = find_similar(installed_apps, "YouTube".lower(), lambda app: app.split(".")[-1].lower())
    if found_app is None or similarity is None or similarity <= 0.5:
        return agent_tool_error(send_whatsapp_message.__name__, message="No application similar to YouTube was found.")

    return frontend_capability(
        kind="open-app-with-intent",
        data={
            "package": found_app,
            "url": f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_query)}",
        }
    )


_repository = create_tool_repository(open_application, send_whatsapp_message, search_on_youtube)
_handlers = create_tool_handlers(lambda tool_call: {
    open_application: [tool_call.function.arguments.get('application_name')],
    send_whatsapp_message: [
        tool_call.function.arguments.get('to'),
        tool_call.function.arguments.get('message')
    ],
    search_on_youtube: [tool_call.function.arguments.get('search_query')]
})

frontend_capabilities_toolkit = Toolkit(
    repository=_repository,
    handlers=_handlers,
)
