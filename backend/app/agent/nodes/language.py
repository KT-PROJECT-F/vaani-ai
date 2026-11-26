"""Detect the language of a message.

Starter version: script-based plus a small word list for romanized Hindi and Telugu.
TODO (Pair 2): improve with an LLM call or a library, and add eval cases for each language.
"""

import re

from app.agent.schemas import Language
from app.agent.state import AgentState

TELUGU_SCRIPT = re.compile(r"[ఀ-౿]")
DEVANAGARI_SCRIPT = re.compile(r"[ऀ-ॿ]")

ROMANIZED_HINDI = {"ghar", "mein", "paani", "nahi", "bhej", "jaldi", "kar", "do", "hai", "chahiye"}
ROMANIZED_TELUGU = {"kavali", "ledu", "pampandi", "ventane", "intlo", "raavatledu", "cheyyandi"}


def detect_language(text: str) -> Language:
    if TELUGU_SCRIPT.search(text):
        return "te"
    if DEVANAGARI_SCRIPT.search(text):
        return "hi"
    words = set(re.findall(r"[a-z]+", text.lower()))
    if len(words & ROMANIZED_HINDI) >= 2 or len(words & ROMANIZED_TELUGU) >= 1:
        return "mixed"
    return "en"


def detect_language_node(state: AgentState) -> AgentState:
    return {"language": detect_language(state["message"])}
