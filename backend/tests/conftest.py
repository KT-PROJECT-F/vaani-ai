import os

import pytest

# Tests never call real LLMs or speech APIs.
os.environ["GROQ_API_KEY"] = ""
os.environ["GOOGLE_API_KEY"] = ""
os.environ["ENABLE_LOCAL_FALLBACKS"] = "false"


@pytest.fixture(autouse=True)
def clear_caches() -> None:
    from app.agent.graph import get_agent
    from app.core.config import get_settings

    get_settings.cache_clear()
    get_agent.cache_clear()
