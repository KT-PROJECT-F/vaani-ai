from typing import TypedDict

from app.agent.schemas import Language, ServiceRequest


class AgentState(TypedDict, total=False):
    message: str
    language: Language
    request: ServiceRequest
    safety_steps: list[str]
    reply: str
