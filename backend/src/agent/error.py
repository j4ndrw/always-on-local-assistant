from dataclasses import asdict, dataclass
from typing import Literal


@dataclass
class AgentToolError:
    error: Literal['agent-tool-error']
    origin: str
    message: str

    def dict(self):
        return {k: v for k, v in asdict(self).items()}

def agent_tool_error(origin: str, *, message: str) -> dict:
    return AgentToolError(error='agent-tool-error', origin=origin, message=message).dict()
