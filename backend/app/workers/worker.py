"""Background jobs with ARQ. Run: arq app.workers.worker.WorkerSettings

TODO (Pair 3, week 6): booking reminders and rating requests (flow F12).
"""

import logging
from typing import Any

from arq.connections import RedisSettings

from app.core.config import get_settings

logger = logging.getLogger(__name__)


async def send_booking_reminder(ctx: dict[str, Any], booking_id: int) -> None:
    logger.info("TODO: send reminder for booking %s", booking_id)


class WorkerSettings:
    functions = [send_booking_reminder]
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
