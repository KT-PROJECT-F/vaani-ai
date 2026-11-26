"""Text to speech with Edge-TTS (free). Returns MP3 bytes, or None if TTS fails.

TODO (Pair 1): cache audio for repeated phrases, and pick the voice from the reply text
when the language is "mixed".
"""

import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def voice_for(language: str) -> str:
    s = get_settings()
    return {"te": s.tts_voice_te, "hi": s.tts_voice_hi}.get(language, s.tts_voice_en)


async def synthesize(text: str, language: str) -> bytes | None:
    try:
        import edge_tts

        communicate = edge_tts.Communicate(text, voice_for(language))
        audio = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
        return bytes(audio) or None
    except Exception:
        logger.exception("TTS failed, replying with text only")
        return None
