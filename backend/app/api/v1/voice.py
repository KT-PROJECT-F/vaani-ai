import base64

from fastapi import APIRouter, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from app.agent.graph import run_agent
from app.api.v1.chat import to_chat_out
from app.schemas.api import VoiceOut
from app.voice.stt import STTUnavailableError, transcribe
from app.voice.tts import synthesize

router = APIRouter()

MAX_AUDIO_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("/voice", response_model=VoiceOut)
async def voice(file: UploadFile) -> VoiceOut:
    audio = await file.read()
    if not audio:
        raise HTTPException(status_code=400, detail="Empty audio file")
    if len(audio) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Audio file too large")

    try:
        transcript = await transcribe(audio, file.filename or "audio.webm")
    except STTUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    if not transcript.text:
        raise HTTPException(status_code=422, detail="Could not hear anything. Try again.")

    state = await run_in_threadpool(run_agent, transcript.text)
    out = to_chat_out(state)
    audio_reply = await synthesize(out.reply, out.language)

    return VoiceOut(
        **out.model_dump(),
        transcript=transcript.text,
        stt_provider=transcript.provider,
        reply_audio_base64=base64.b64encode(audio_reply).decode() if audio_reply else None,
    )
