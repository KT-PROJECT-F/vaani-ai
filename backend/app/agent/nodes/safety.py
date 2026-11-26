"""Return safety steps before anything else when a request sounds dangerous.

TODO (Pair 2): translate steps into the user's language and add more hazards.
"""

from app.agent.nodes.extract import contains_any
from app.agent.state import AgentState

HAZARDS: dict[str, tuple[list[str], list[str]]] = {
    "gas": (
        ["gas", "గ్యాస్", "गैस"],
        [
            "Do not switch any lights or appliances on or off.",
            "Turn off the gas cylinder regulator.",
            "Open all doors and windows.",
            "Leave the house and call 1906 (LPG emergency) if the smell is strong.",
        ],
    ),
    "electric": (
        ["spark", "shock", "smoke", "fire", "షాక్"],
        [
            "Switch off the main power supply if it is safe to reach.",
            "Do not touch wires or switches with wet hands.",
            "Keep children away from the area.",
            "Call 101 (fire) if there is fire or heavy smoke.",
        ],
    ),
}


def safety_check_node(state: AgentState) -> AgentState:
    lowered = state["message"].lower()
    steps: list[str] = []
    for words, hazard_steps in HAZARDS.values():
        if contains_any(lowered, words):
            steps.extend(hazard_steps)
    if not steps:
        return {"safety_steps": []}
    request = state["request"].model_copy(update={"urgency": "emergency"})
    return {"safety_steps": steps, "request": request}
