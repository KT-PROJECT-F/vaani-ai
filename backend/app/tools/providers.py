"""Provider search tool.

TODO (Pair 3): filter by area and free slots, rank by rating and distance, and wrap
this as a LangChain tool for the agent (week 4).
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Provider


def search_providers(db: Session, service: str, city: str, limit: int = 5) -> list[Provider]:
    stmt = (
        select(Provider)
        .where(
            Provider.service_code == service,
            Provider.city == city,
            Provider.is_active.is_(True),
        )
        .order_by(Provider.rating.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt))
