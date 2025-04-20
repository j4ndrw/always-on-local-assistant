import urllib.parse
from dataclasses import asdict, dataclass, field
from typing import Any

from ....settings.settings import settings
from ....utils import find_similar
from ...tools.tools import define_toolkit, description
from ..utils import get_application_util

tool, resource, register_toolkit = define_toolkit()


@dataclass
class FrontendCapability:
    kind: str
    data: dict[str, Any]
    archetype: str = field(default_factory=lambda: "frontend-capability")

    def dict(self):
        return {k: v for k, v in asdict(self).items()}


def frontend_capability(*, kind: str, data: dict[str, Any]) -> dict:
    return FrontendCapability(kind=kind, data=data).dict()


@tool.create(
    description=description(
        """
        Opens the application on the user's phone (e.g. YouTube, Whatsapp, etc...)
        NOTE: Only use this tool if the user **explicitely** asks for an app to be opened.
        """,
        args=[
            (
                "application_name",
                "The name of the application that needs to be opened (e.g. YouTube, Whatsapp, etc...)",
            )
        ],
        returns=[
            (
                "dict",
                "A JSON object, containing the url of the application that needs to be opened",
            )
        ],
    ),
)
def open_application(application_name: str) -> dict:
    if not application_name:
        return tool.error(
            open_application.__name__, error="No application name provided."
        )

    app, err = get_application_util(
        open_application.__name__, app_name=application_name
    )
    if err:
        return err

    return frontend_capability(kind="open-app", data={"url": app})


@tool.create(
    description=description(
        """
        Sends a WhatsApp message to a contact.
        NOTE: Only use this tool if the user **explicitely** asks for a message to be sent to a contact.
        IMPORTANT: This tool only prepares the message to be sent. It is only sent if the user approves the action.
        """,
        args=[
            ("to", "The name of the contact that the user wants to send a message to"),
            ("message", "The message to send to the contact"),
        ],
        returns=[
            (
                "dict",
                "A JSON object, containing the url of the WhatsApp application that needs to be opened with the appropriate parameters so that the message can be sent.",
            )
        ],
    ),
)
def send_whatsapp_message(to: str, message: str) -> dict:
    if not to:
        return tool.error(
            send_whatsapp_message.__name__, error="No recipient provided."
        )

    if not message:
        return tool.error(
            send_whatsapp_message.__name__,
            error="No message to send to recipient was provided.",
        )

    app, err = get_application_util(send_whatsapp_message.__name__, app_name="WhatsApp")
    if err:
        return err

    contacts_map: dict[str, str] = settings.metadata.get("contacts", {})
    if len(contacts_map.keys()) == 0:
        return tool.error(
            send_whatsapp_message.__name__,
            error="No contacts found on the user's device",
        )

    found_contact, similarity = find_similar(
        contacts_map.keys(), to.lower(), lambda contact: contact.lower()
    )
    if found_contact is None or similarity is None or similarity <= 0.2:
        return tool.error(
            send_whatsapp_message.__name__,
            error=f"No contact similar to {to} was found.",
        )

    phone_number = contacts_map.get(found_contact, None)
    if phone_number is None:
        return tool.error(
            send_whatsapp_message.__name__,
            error=f"Contact {found_contact} has no phone number associated to it.",
        )

    return frontend_capability(
        kind="open-app-with-intent",
        data={
            "package": app,
            "url": f"https://api.whatsapp.com/send?phone={phone_number}&text={message}",
        },
    )


@tool.create(
    description=description(
        """
        Searches for videos on the YouTube app.
        NOTE: Only use this tool if the user **explicitely** asks you to search for something on YouTube.
        """,
        args=[("search_query", "The thing the user wants to search for on YouTube")],
        returns=[
            (
                "dict",
                "A list of JSON object, containing the url of the YouTube application that needs to be opened with the appropriate parameters.",
            )
        ],
    ),
)
def search_on_youtube(search_query: str) -> dict:
    if not search_query:
        return tool.error(search_on_youtube.__name__, error="No search query provided")

    app, err = get_application_util(search_on_youtube.__name__, app_name="YouTube")
    if err:
        return err

    return frontend_capability(
        kind="open-app-with-intent",
        data={
            "package": app,
            "url": f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(search_query)}",
        },
    )
