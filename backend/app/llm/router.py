"""LLM router: Groq -> Gemini -> Ollama (local, optional).

Each provider is tried in order. If none is configured, callers get None and fall back
to rule-based logic, so the app runs without any API keys.
"""

import logging
from pathlib import Path
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.schemas import ServiceRequest
from app.core.config import get_settings

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "agent" / "prompts"


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def get_chat_models(kind: str = "fast") -> list[BaseChatModel]:
    """Return configured chat models in fallback order. kind: "fast" or "smart"."""
    s = get_settings()
    models: list[BaseChatModel] = []

    if s.groq_api_key:
        from langchain_groq import ChatGroq

        model = s.groq_model_fast if kind == "fast" else s.groq_model_smart
        models.append(
            ChatGroq(  # type: ignore[call-arg]
                model=model, api_key=s.groq_api_key, timeout=20, max_retries=1
            )
        )

    if s.google_api_key:
        from langchain_google_genai import ChatGoogleGenerativeAI

        models.append(ChatGoogleGenerativeAI(model=s.gemini_model, google_api_key=s.google_api_key))

    if s.enable_local_fallbacks:
        from langchain_ollama import ChatOllama

        models.append(ChatOllama(model=s.ollama_model, base_url=s.ollama_base_url))

    return models


def invoke_structured(schema: type[Any], system_prompt: str, user_text: str) -> Any:
    """Try each model in order until one returns valid structured output."""
    models = get_chat_models("fast")
    if not models:
        raise RuntimeError("No LLM configured")

    messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_text)]
    last_error: Exception | None = None
    for model in models:
        try:
            return model.with_structured_output(schema).invoke(messages)
        except Exception as exc:  # noqa: BLE001 - try the next provider
            logger.warning("LLM %s failed: %s", type(model).__name__, exc)
            last_error = exc
    raise RuntimeError("All LLM providers failed") from last_error


def make_structured_extractor() -> Any:
    """Return a function text -> ServiceRequest, or None if no LLM is configured."""
    if not get_chat_models():
        logger.info("No LLM keys set: using rule-based extractor")
        return None
    prompt = load_prompt("extract")

    def extractor(text: str) -> ServiceRequest:
        result = invoke_structured(ServiceRequest, prompt, text)
        if not isinstance(result, ServiceRequest):
            result = ServiceRequest.model_validate(result)
        return result

    return extractor
