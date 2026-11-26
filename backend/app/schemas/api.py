"""Request and response models for the public API. Frontend types mirror these."""

from pydantic import BaseModel, ConfigDict, Field

from app.agent.schemas import Language, ServiceRequest


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str | None = None


class ChatOut(BaseModel):
    reply: str
    language: Language
    request: ServiceRequest
    safety_steps: list[str] = []
    price_range: tuple[int, int] | None = None


class VoiceOut(ChatOut):
    transcript: str
    stt_provider: str
    reply_audio_base64: str | None = None


class ProviderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    service_code: str
    city: str
    area: str
    rating: float
    price_min: int
    price_max: int
