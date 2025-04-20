import subprocess
from typing import Literal

from src.agent.tools.tools import define_toolkit, description

# FIXME(j4ndrw): Not registering toolkit, since I don't currently
# know how to help the LLM distinguish between tools that need to be used
# on the mobile device and tools that need to be used on the computer.
tool, _, _ = define_toolkit()


@tool.create(
    description=description(
        """
        Opens the user's browser on their computer.
        NOTE: Only use this tool if the user **explicitely** asks for the browser to be opened on their computer!
        NOTE: Only open the browser if the kind is specified.
        """,
        args=[("kind", "The browser kind to open. Can be `personal` or `work`.")],
        returns=[("dict", "A JSON object, containing an error or a success status")],
    )
)
def open_browser_on_computer(kind: Literal["personal"] | Literal["work"] | str) -> dict:
    if kind != "personal" and kind != "work":
        return tool.error(
            open_browser_on_computer.__name__,
            error="The browser kind was not specified. Should be `personal` or `work`",
        )

    try:
        browser_to_open = "brave-browser" if kind == "personal" else "google-chrome"
        subprocess.Popen([browser_to_open])
        return tool.success(open_browser_on_computer.__name__)
    except Exception as e:
        if hasattr(e, "message"):
            return tool.error(
                open_browser_on_computer.__name__,
                error=f"Could not open the user's browser. Reason: {e.message}",  # pyright: ignore
            )
        else:
            return tool.error(
                open_browser_on_computer.__name__,
                error=f"Could not open the user's browser. Something went wrong",
            )


@tool.create(
    description=description(
        """
        Plays some jazz in the user's personal browser
        NOTE: Only use this tool if the user **explicitely** asks for the some jazz to be played.
        """,
        returns=[("dict", "A JSON object, containing an error or a success status")],
    )
)
def play_some_jazz_on_computer() -> dict:
    song = "https://www.youtube.com/watch?v=i-8dosPqLE4"
    try:
        browser_to_open = "brave-browser"
        subprocess.Popen([browser_to_open, song])
        return tool.success(play_some_jazz_on_computer.__name__)
    except Exception as e:
        if hasattr(e, "message"):
            return tool.error(
                play_some_jazz_on_computer.__name__,
                error=f"Could not play jazz. Reason: {e.message}",  # pyright: ignore
            )
        else:
            return tool.error(
                play_some_jazz_on_computer.__name__,
                error=f"Could not play jazz. Something went wrong",
            )
