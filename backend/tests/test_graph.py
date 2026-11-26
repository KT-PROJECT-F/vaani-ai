from app.agent.graph import build_graph
from app.agent.schemas import ServiceRequest


def test_graph_with_rule_based_extractor() -> None:
    result = build_graph().invoke({"message": "Need a plumber in Guntur today"})
    assert result["language"] == "en"
    assert result["request"].service == "plumber"
    assert "Guntur" in result["reply"]


def test_graph_uses_injected_extractor() -> None:
    def fake_llm(text: str) -> ServiceRequest:
        return ServiceRequest(service="carpenter", city="Tirupati", urgency="flexible")

    result = build_graph(fake_llm).invoke({"message": "anything"})
    assert result["request"].service == "carpenter"


def test_graph_falls_back_when_extractor_fails() -> None:
    def broken(text: str) -> ServiceRequest:
        raise TimeoutError("rate limited")

    result = build_graph(broken).invoke({"message": "electrician in Hyderabad"})
    assert result["request"].service == "electrician"


def test_safety_first_for_gas() -> None:
    result = build_graph().invoke({"message": "I smell gas in my kitchen in Vijayawada"})
    assert result["request"].urgency == "emergency"
    assert result["safety_steps"]
    assert result["reply"].startswith("Safety first")


def test_asks_for_city_in_telugu() -> None:
    result = build_graph().invoke({"message": "ప్లంబర్ కావాలి"})
    assert result["language"] == "te"
    assert "ఊరు" in result["reply"]
