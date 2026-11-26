"""Seed services, ~200 sample providers and 7 days of slots. Safe to run more than once.

Run from the backend folder:  python ../scripts/seed_providers.py
All names and phone numbers are fake sample data.
"""

import random
import sys
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from sqlalchemy import delete  # noqa: E402

from app.db.models import Booking, Provider, ProviderSlot, Service  # noqa: E402
from app.db.session import get_session_factory  # noqa: E402
from app.tools.pricing import BASE_PRICES  # noqa: E402

IST = ZoneInfo("Asia/Kolkata")

SERVICES = {
    "plumber": "Plumber",
    "electrician": "Electrician",
    "water_tanker": "Water tanker",
    "ac_repair": "AC repair",
    "carpenter": "Carpenter",
    "house_cleaning": "House cleaning",
    "pest_control": "Pest control",
    "appliance_repair": "Appliance repair",
    "ro_service": "RO purifier service",
    "painter": "Painter",
}

AREAS = {
    "Hyderabad": ["Madhapur", "Gachibowli", "Kukatpally", "Ameerpet", "Dilsukhnagar"],
    "Vijayawada": ["Benz Circle", "Patamata", "Governorpet", "Moghalrajpuram", "Gunadala"],
    "Guntur": ["Brodipet", "Arundelpet", "Lakshmipuram", "Pattabhipuram", "Korritepadu"],
    "Visakhapatnam": ["MVP Colony", "Dwaraka Nagar", "Gajuwaka", "Madhurawada", "Seethammadhara"],
    "Tirupati": ["Tilak Road", "Korlagunta", "Bairagipatteda", "Renigunta Road", "SV Nagar"],
}

FIRST = ["Ravi", "Suresh", "Kiran", "Venkat", "Srinivas", "Prasad", "Ramesh", "Anil", "Mahesh",
         "Naresh", "Lakshmi", "Padma", "Swathi", "Rajesh", "Gopi", "Satish"]
LAST = ["Reddy", "Rao", "Naidu", "Kumar", "Varma", "Sharma", "Chowdary", "Babu"]


def main() -> None:
    rng = random.Random(42)
    session = get_session_factory()()
    with session.begin():
        session.execute(delete(Booking))
        session.execute(delete(ProviderSlot))
        session.execute(delete(Provider))
        session.execute(delete(Service))
        session.add_all(Service(code=c, name=n) for c, n in SERVICES.items())
        session.flush()

        today = datetime.now(IST).date()
        count = 0
        for city, areas in AREAS.items():
            for service in SERVICES:
                for _ in range(4):
                    low, high = BASE_PRICES[service]
                    provider = Provider(
                        name=f"{rng.choice(FIRST)} {rng.choice(LAST)}",
                        phone=f"+91 90000 {rng.randint(10000, 99999)}",
                        service_code=service,
                        city=city,
                        area=rng.choice(areas),
                        rating=round(rng.uniform(3.5, 5.0), 1),
                        price_min=low,
                        price_max=high,
                    )
                    session.add(provider)
                    session.flush()
                    for day in range(7):
                        for hour in (8, 10, 12, 14, 16, 18):
                            start = datetime.combine(today + timedelta(days=day), time(hour), IST)
                            session.add(
                                ProviderSlot(
                                    provider_id=provider.id,
                                    starts_at=start,
                                    ends_at=start + timedelta(hours=2),
                                )
                            )
                    count += 1
    print(f"Seeded {len(SERVICES)} services and {count} providers.")


if __name__ == "__main__":
    main()
