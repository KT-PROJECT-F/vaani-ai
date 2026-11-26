"""Starter data model. Pair 3 adds Address, Rating, ManualTicket with Alembic migrations."""

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class Service(Base):
    __tablename__ = "services"

    code: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(80))


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(20))
    service_code: Mapped[str] = mapped_column(ForeignKey("services.code"), index=True)
    city: Mapped[str] = mapped_column(String(60), index=True)
    area: Mapped[str] = mapped_column(String(120))
    rating: Mapped[float] = mapped_column(Float, default=4.0)
    price_min: Mapped[int] = mapped_column(Integer)
    price_max: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    slots: Mapped[list["ProviderSlot"]] = relationship(back_populates="provider")


class ProviderSlot(Base):
    __tablename__ = "provider_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False)

    provider: Mapped[Provider] = relationship(back_populates="slots")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True)
    telegram_id: Mapped[str | None] = mapped_column(String(40), unique=True)
    name: Mapped[str | None] = mapped_column(String(120))
    preferred_language: Mapped[str] = mapped_column(String(10), default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"))
    slot_id: Mapped[int] = mapped_column(ForeignKey("provider_slots.id"), unique=True)
    service_code: Mapped[str] = mapped_column(ForeignKey("services.code"))
    problem: Mapped[str] = mapped_column(Text, default="")
    urgency: Mapped[str] = mapped_column(String(20))
    city: Mapped[str] = mapped_column(String(60))
    area: Mapped[str | None] = mapped_column(String(120))
    # pending, confirmed, rescheduled, cancelled, completed, failed (see docs/business-rules.md)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
