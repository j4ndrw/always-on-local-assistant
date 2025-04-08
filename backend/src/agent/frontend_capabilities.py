from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher
from typing import Any

from ..settings.settings import settings

from .agent import Toolkit, create_tool_handlers, create_tool_repository

Todos = dict[str, bool]
todos: Todos = {}


@dataclass
class FrontendCapability:
    kind: str
    data: dict[str, Any]
    archetype: str = field(default_factory=lambda: "frontend-capability")

    def dict(self):
        return {k: v for k, v in asdict(self).items()}

def open_application(application_name: str) -> dict:
    """
    Opens the application on the user's phone (e.g. YouTube, Whatsapp, etc...)
    NOTE: Only use this tool if the user **explicitely** asks for an app to be opened.

    Args:
        application_name: The name of the application that needs to be opened (e.g. YouTube, Whatsapp, etc...)

    Returns:
        dict: A JSON object, containing the url of the application that needs to be opened
    """
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    installed_apps: list[str] = settings.metadata.get("installedApps", [])
    if len(installed_apps) == 0:
        return FrontendCapability(kind="open-app", data={}).dict()

    apps_with_similarities: list[tuple[str, float]] = []
    for app in installed_apps:
        apps_with_similarities.append((app, similar(application_name.lower(), app.split(".")[-1].lower())))

    found_app, similarity = sorted(apps_with_similarities, key=lambda x: x[1])[-1]
    if similarity > 0.5:
        return FrontendCapability(kind="open-app", data={"url": found_app}).dict()
    return FrontendCapability(kind="open-app", data={}).dict()

_repository = create_tool_repository(open_application)
_handlers = create_tool_handlers(lambda tool_call: {
    open_application: [tool_call.function.arguments.get('application_name')]
})

frontend_capabilities_toolkit = Toolkit(
    repository=_repository,
    handlers=_handlers,
)
