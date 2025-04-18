from dataclasses import asdict, dataclass, field


@dataclass
class AgentToolSuccess:
    origin: str
    success: bool = field(default_factory=lambda: True)

    def dict(self):
        return {k: v for k, v in asdict(self).items()}

def agent_tool_success(origin: str) -> dict:
    return AgentToolSuccess(origin=origin).dict()
