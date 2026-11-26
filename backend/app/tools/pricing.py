"""Price estimate tool. Starter prices are rough sample ranges in rupees for a basic visit.

TODO (Pair 3): move to the database, vary by city, add an overcharge warning.
"""

BASE_PRICES: dict[str, tuple[int, int]] = {
    "plumber": (200, 600),
    "electrician": (200, 600),
    "water_tanker": (500, 1200),
    "ac_repair": (400, 1500),
    "carpenter": (300, 900),
    "house_cleaning": (1500, 4000),
    "pest_control": (800, 2500),
    "appliance_repair": (300, 1200),
    "ro_service": (300, 800),
    "painter": (2000, 8000),
}

CITY_MULTIPLIER: dict[str, float] = {"Hyderabad": 1.2, "Visakhapatnam": 1.1}


def estimate_price(service: str, city: str) -> tuple[int, int] | None:
    base = BASE_PRICES.get(service)
    if base is None:
        return None
    m = CITY_MULTIPLIER.get(city, 1.0)
    return round(base[0] * m), round(base[1] * m)
