# Architecture

## Components

| Component | Folder | Owner |
|---|---|---|
| React web app and admin dashboard | `frontend/` | Pair 4 |
| FastAPI backend (REST, uploads, Telegram webhook) | `backend/app/api/`, `backend/app/main.py` | Pair 3 |
| Voice service (STT, TTS) | `backend/app/voice/` | Pair 1 |
| Telegram channel | `backend/app/channels/` | Pair 1 |
| LangGraph agent | `backend/app/agent/` | Pair 2 |
| LLM router (Groq, Gemini, Ollama) | `backend/app/llm/` | Pair 2 |
| Agent tools (providers, pricing, booking, reminders) | `backend/app/tools/` | Pair 3 |
| Database models and migrations | `backend/app/db/`, `backend/alembic/` | Pair 3 |
| Background jobs (ARQ) | `backend/app/workers/` | Pair 3 |
| Evals | `evals/` | Pair 2 |

## Request flow

```
client (text | audio | photo)
  -> FastAPI
  -> STT (audio) or vision (photo)
  -> LangGraph agent
  -> tools (DB, pricing, booking)
  -> reply text
  -> TTS
  -> client
```

## Agent graph (target by week 5)

```
route_input -> detect_language -> classify_intent
   -> extract_details -> safety_check
   -> clarify (interrupt, max 3) or search_providers
   -> estimate_price -> confirm_with_user (interrupt)
   -> book_slot -> respond
manage_booking handles reschedule / cancel / status
fallback handles any failure
```

The starter code implements: `detect_language -> extract_details -> safety_check -> respond`.

## Fallback chains

- LLM: Groq -> Gemini -> Ollama (only if `ENABLE_LOCAL_FALLBACKS=true`) -> rule-based extractor
- STT: Groq Whisper -> faster-whisper (local)
- TTS: Edge-TTS -> text only

## Data model (starter)

`Service`, `Provider`, `ProviderSlot`, `User`, `Booking`. More models (`Address`, `Rating`, `ManualTicket`) are added by Pair 3 with Alembic migrations.
