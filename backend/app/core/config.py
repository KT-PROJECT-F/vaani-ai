"""All settings come from environment variables or the .env file.

Never read os.environ directly anywhere else.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173"

    # Database and cache
    database_url: str = "postgresql+psycopg://vaani:vaani@localhost:5432/vaani"
    redis_url: str = "redis://localhost:6379/0"

    # LLMs
    groq_api_key: str = ""
    groq_model_fast: str = "openai/gpt-oss-20b"
    groq_model_smart: str = "openai/gpt-oss-120b"
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # Local fallbacks (16 GB laptops only)
    enable_local_fallbacks: bool = False
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    whisper_local_model: str = "small"

    # Speech
    groq_whisper_model: str = "whisper-large-v3"
    tts_voice_te: str = "te-IN-ShrutiNeural"
    tts_voice_hi: str = "hi-IN-SwaraNeural"
    tts_voice_en: str = "en-IN-NeerjaNeural"

    # Observability
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"

    # Telegram
    telegram_bot_token: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
