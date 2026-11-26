import pytest

from app.agent.nodes.language import detect_language


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("My sink is leaking", "en"),
        ("మా ఇంట్లో కరెంట్ పోయింది", "te"),
        ("मेरे घर की बिजली चली गई", "hi"),
        ("Ghar mein paani nahi aa raha", "mixed"),
        ("Plumber ventane kavali", "mixed"),
    ],
)
def test_detect_language(text: str, expected: str) -> None:
    assert detect_language(text) == expected
