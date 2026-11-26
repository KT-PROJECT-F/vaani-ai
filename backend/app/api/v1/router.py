from fastapi import APIRouter

from app.api.v1 import chat, providers, voice

api_router = APIRouter()
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(voice.router, tags=["voice"])
api_router.include_router(providers.router, tags=["providers"])

# TODO (Pair 3): bookings.py, auth.py (mock OTP), admin.py
# TODO (Pair 1): image.py (photo diagnosis, week 6)
