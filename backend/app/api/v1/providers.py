from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.api import ProviderOut
from app.tools.providers import search_providers

router = APIRouter()


@router.get("/providers", response_model=list[ProviderOut])
def list_providers(
    db: Annotated[Session, Depends(get_db)],
    service: Annotated[str, Query(examples=["plumber"])],
    city: Annotated[str, Query(examples=["Vijayawada"])],
    limit: Annotated[int, Query(ge=1, le=50)] = 5,
) -> list[ProviderOut]:
    providers = search_providers(db, service=service, city=city, limit=limit)
    return [ProviderOut.model_validate(p) for p in providers]
