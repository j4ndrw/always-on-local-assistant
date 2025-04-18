from ..utils import find_similar
from ..settings.settings import settings
from .error import AgentToolError, agent_tool_error


def get_application_util(origin: str, *, app_name: str) -> tuple[str | None, dict | None]:
    installed_apps: list[str] = settings.metadata.get("installedApps", [])
    if len(installed_apps) == 0:
        return None, agent_tool_error(origin, message="No applications installed on the user's device.")

    found_app, similarity = find_similar(installed_apps, app_name.lower(), lambda app: app.split(".")[-1].lower())
    if found_app is None or similarity is None or similarity <= 0.5:
        return None, agent_tool_error(origin, message=f"No application similar to {app_name} was found.")

    return found_app, None
