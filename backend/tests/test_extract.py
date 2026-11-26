from app.agent.nodes.extract import rule_based_extract


def test_english_sample() -> None:
    r = rule_based_extract(
        "My kitchen sink is leaking badly and water is all over the floor. "
        "I need a plumber urgently this evening at Benz Circle, Vijayawada."
    )
    assert r.service == "plumber"
    assert r.city == "Vijayawada"
    assert r.urgency == "today"
    assert r.time_window == "evening"


def test_telugu_sample() -> None:
    r = rule_based_extract("మా ఇంట్లో కరెంట్ పోయింది, ఫ్యూజ్ ఎగిరిపోయింది. ఒక ఎలక్ట్రీషియన్‌ని గుంటూరుకి పంపండి, ఈరోజే కావాలి.")
    assert r.service == "electrician"
    assert r.city == "Guntur"
    assert r.urgency == "today"


def test_mixed_sample() -> None:
    r = rule_based_extract(
        "Ghar mein paani nahi aa raha, please ek water tanker bhej do jaldi, Madhapur, Hyderabad."
    )
    assert r.service == "water_tanker"
    assert r.city == "Hyderabad"
    assert r.urgency == "today"


def test_word_boundaries() -> None:
    r = rule_based_extract("I know my account details are correct.")
    assert r.service == "unknown"
    assert r.urgency == "flexible"


def test_missing_city() -> None:
    r = rule_based_extract("Need an electrician")
    assert r.missing_fields() == ["city"]
