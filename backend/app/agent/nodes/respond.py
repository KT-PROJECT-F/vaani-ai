"""Compose the reply in the user's language.

Starter version: templates. Clarifying questions are asked inline.
TODO (Pair 2): replace with the clarify node (LangGraph interrupt) and LLM-written replies.
"""

from app.agent.schemas import Language
from app.agent.state import AgentState

TEMPLATES: dict[str, dict[str, str]] = {
    "en": {
        "ask_service": "What service do you need? For example plumber, electrician or tanker.",
        "ask_city": "Which city and area are you in?",
        "ok": "Got it. Looking for a {service} in {city} ({urgency}).",
    },
    "te": {
        "ask_service": "మీకు ఏ సర్వీస్ కావాలి? ఉదాహరణకు ప్లంబర్, ఎలక్ట్రీషియన్ లేదా వాటర్ ట్యాంకర్.",
        "ask_city": "మీరు ఏ ఊరు, ఏ ఏరియాలో ఉన్నారు?",
        "ok": "సరే, {city}లో {service} కోసం వెతుకుతున్నాను ({urgency}).",
    },
    "hi": {
        "ask_service": "आपको कौन सी सर्विस चाहिए? जैसे प्लंबर, इलेक्ट्रीशियन या पानी का टैंकर।",
        "ask_city": "आप किस शहर और इलाके में हैं?",
        "ok": "ठीक है, {city} में {service} ढूंढ रहे हैं ({urgency})।",
    },
}


def _templates_for(language: Language) -> dict[str, str]:
    # Mixed (romanized) messages get English replies for now.
    return TEMPLATES.get(language, TEMPLATES["en"])


def respond_node(state: AgentState) -> AgentState:
    t = _templates_for(state.get("language", "en"))
    request = state["request"]
    missing = request.missing_fields()

    if "service" in missing:
        reply = t["ask_service"]
    elif "city" in missing:
        reply = t["ask_city"]
    else:
        reply = t["ok"].format(
            service=request.service.replace("_", " "),
            city=request.city,
            urgency=request.urgency,
        )

    steps = state.get("safety_steps") or []
    if steps:
        reply = "\n".join(["Safety first:", *[f"- {s}" for s in steps], "", reply])
    return {"reply": reply}
