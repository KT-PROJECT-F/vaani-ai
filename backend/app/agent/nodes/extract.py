"""Extract a structured ServiceRequest from the user's message.

Uses the LLM extractor when API keys are set, otherwise a rule-based extractor so the
app works on day 1 without any keys.
"""

import logging
import re
from collections.abc import Callable

from app.agent.schemas import ServiceRequest, ServiceType, Urgency
from app.agent.state import AgentState

logger = logging.getLogger(__name__)

Extractor = Callable[[str], ServiceRequest]

# Order matters: more specific services first.
SERVICE_KEYWORDS: list[tuple[ServiceType, list[str]]] = [
    ("water_tanker", ["tanker", "paani nahi", "water not coming", "ట్యాంకర్"]),
    (
        "electrician",
        [
            "electrician",
            "fuse",
            "current",
            "power cut",
            "switch",
            "wiring",
            "bijli",
            "కరెంట్",
            "ఎలక్ట్రీషియన్",
            "बिजली",
        ],
    ),
    ("plumber", ["plumber", "leak", "sink", "tap", "pipe", "drain", "ప్లంబర్", "नल"]),
    ("ac_repair", ["ac", "air conditioner", "not cooling", "ఏసీ"]),
    ("carpenter", ["carpenter", "door", "furniture", "wood"]),
    ("house_cleaning", ["cleaning", "deep clean", "maid"]),
    ("pest_control", ["pest", "cockroach", "termite", "rats", "mosquito"]),
    ("appliance_repair", ["washing machine", "fridge", "refrigerator", "microwave"]),
    ("ro_service", ["ro", "purifier", "water filter"]),
    ("painter", ["paint", "painter", "wall colour", "wall color"]),
]

CITY_KEYWORDS: dict[str, list[str]] = {
    "Hyderabad": ["hyderabad", "హైదరాబాద్", "हैदराबाद"],
    "Vijayawada": ["vijayawada", "bezawada", "విజయవాడ"],
    "Guntur": ["guntur", "గుంటూరు"],
    "Visakhapatnam": ["visakhapatnam", "vizag", "విశాఖ"],
    "Tirupati": ["tirupati", "తిరుపతి"],
}

EMERGENCY_WORDS = ["gas", "spark", "shock", "fire", "smoke", "flood", "గ్యాస్", "షాక్"]
TODAY_WORDS = [
    "urgent",
    "today",
    "now",
    "asap",
    "jaldi",
    "tonight",
    "this evening",
    "ventane",
    "ఈరోజే",
    "ఇప్పుడే",
    "अभी",
    "आज",
]
TIME_WORDS = {
    "morning": "morning",
    "afternoon": "afternoon",
    "evening": "evening",
    "tonight": "evening",
    "now": "now",
    "jaldi": "now",
    "ఈరోజే": "today",
}


def contains(text: str, word: str) -> bool:
    """English words match whole words plus simple endings ("leak" matches "leaking",
    but "now" does not match "know" and "ac" does not match "account").
    Telugu and Hindi words match as substrings, because suffixes attach to them
    (for example గుంటూరుకి contains గుంటూరు)."""
    if word.isascii():
        return re.search(rf"\b{re.escape(word)}(s|es|ing|ed)?\b", text) is not None
    return word in text


def contains_any(text: str, words: list[str]) -> bool:
    return any(contains(text, w) for w in words)


def rule_based_extract(text: str) -> ServiceRequest:
    lowered = text.lower()
    service: ServiceType = "unknown"
    for candidate, words in SERVICE_KEYWORDS:
        if contains_any(lowered, words):
            service = candidate
            break

    city = next(
        (name for name, words in CITY_KEYWORDS.items() if contains_any(lowered, words)),
        None,
    )

    urgency: Urgency
    if contains_any(lowered, EMERGENCY_WORDS):
        urgency = "emergency"
    elif contains_any(lowered, TODAY_WORDS):
        urgency = "today"
    else:
        urgency = "flexible"

    time_window = next((v for k, v in TIME_WORDS.items() if contains(lowered, k)), None)

    return ServiceRequest(
        service=service,
        problem=text.strip()[:200],
        urgency=urgency,
        city=city,
        time_window=time_window,
    )


def extract_details_node(state: AgentState, extractor: Extractor | None) -> AgentState:
    text = state["message"]
    if extractor is not None:
        try:
            return {"request": extractor(text)}
        except Exception:
            logger.exception("LLM extraction failed, using rule-based extractor")
    return {"request": rule_based_extract(text)}
