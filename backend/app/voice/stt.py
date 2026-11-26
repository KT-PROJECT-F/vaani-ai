"""Speech to text: Groq Whisper (free tier) -> faster-whisper (local, 16 GB laptops only).

TODO (Pair 1): return a confidence score so the agent can ask the user to confirm
unclear transcripts (flow F5), and measure latency.
"""

import asyncio
import logging
import tempfile
from dataclasses import dataclass

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class STTUnavailableError(RuntimeError):
    pass


@dataclass
class Transcript:
    text: str
    language: str | None
    provider: str


async def _groq_transcribe(audio: bytes, filename: str) -> Transcript:
    from groq import AsyncGroq

    s = get_settings()
    client = AsyncGroq(api_key=s.groq_api_key, timeout=30)
    result = await client.audio.transcriptions.create(
        file=(filename, audio),
        model=s.groq_whisper_model,
        response_format="verbose_json",
    )
    return Transcript(
        text=result.text.strip(),
        language=getattr(result, "language", None),
        provider="groq-whisper",
    )


def _local_transcribe(audio: bytes, filename: str) -> Transcript:
    from faster_whisper import WhisperModel

    s = get_settings()
    suffix = "." + filename.rsplit(".", 1)[-1] if "." in filename else ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix) as f:
        f.write(audio)
        f.flush()
        model = WhisperModel(s.whisper_local_model, compute_type="int8")
        segments, info = model.transcribe(f.name)
        text = " ".join(seg.text for seg in segments).strip()
    return Transcript(text=text, language=info.language, provider="faster-whisper")


async def transcribe(audio: bytes, filename: str = "audio.webm") -> Transcript:
    s = get_settings()
    if s.groq_api_key:
        try:
            return await _groq_transcribe(audio, filename)
        except Exception:
            logger.exception("Groq Whisper failed")
    if s.enable_local_fallbacks:
        return await asyncio.to_thread(_local_transcribe, audio, filename)
    raise STTUnavailableError("No speech-to-text provider available. Set GROQ_API_KEY.")
