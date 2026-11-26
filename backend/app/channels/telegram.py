"""Telegram channel (week 6, Pair 1).

Plan:
1. Create a bot with @BotFather, put the token in TELEGRAM_BOT_TOKEN.
2. For local dev, use long polling (python-telegram-bot or plain httpx getUpdates).
3. For the deployed demo, set the webhook to https://<render-url>/telegram/webhook.
4. Text -> run_agent; voice note -> download file -> transcribe -> run_agent;
   photo -> image diagnosis (week 6).
"""

import logging
from typing import Any

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook")
async def telegram_webhook(update: dict[str, Any]) -> dict[str, bool]:
    logger.info("Telegram update received (not handled yet): %s", update.get("update_id"))
    return {"ok": True}
