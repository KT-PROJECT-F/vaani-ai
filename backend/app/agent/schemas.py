"""The structured output the agent extracts from every request."""

from typing import Literal

from pydantic import BaseModel, Field

ServiceType = Literal[
    "plumber",
    "electrician",
    "water_tanker",
    "ac_repair",
    "carpenter",
    "house_cleaning",
    "pest_control",
    "appliance_repair",
    "ro_service",
    "painter",
    "unknown",
]

Urgency = Literal["emergency", "today", "flexible"]

Language = Literal["en", "te", "hi", "mixed"]

SUPPORTED_CITIES = ["Hyderabad", "Vijayawada", "Guntur", "Visakhapatnam", "Tirupati"]


class ServiceRequest(BaseModel):
    service: ServiceType = Field("unknown", description="Which home service is needed")
    problem: str = Field("", description="Short English summary of the problem")
    urgency: Urgency = Field("flexible", description="emergency, today or flexible")
    city: str | None = Field(None, description=f"One of {SUPPORTED_CITIES}, or null")
    area: str | None = Field(None, description="Locality or landmark inside the city")
    time_window: str | None = Field(
        None, description="morning, afternoon, evening, now, or a specific time"
    )

    def missing_fields(self) -> list[str]:
        missing: list[str] = []
        if self.service == "unknown":
            missing.append("service")
        if not self.city:
            missing.append("city")
        return missing
