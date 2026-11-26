from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_chat() -> None:
    r = client.post("/api/v1/chat", json={"message": "Need an electrician in Guntur now"})
    assert r.status_code == 200
    body = r.json()
    assert body["request"]["service"] == "electrician"
    assert body["request"]["city"] == "Guntur"
    assert body["price_range"] == [200, 600]


def test_chat_rejects_empty_message() -> None:
    r = client.post("/api/v1/chat", json={"message": ""})
    assert r.status_code == 422


def test_voice_without_stt_returns_503() -> None:
    r = client.post("/api/v1/voice", files={"file": ("a.webm", b"fake-audio", "audio/webm")})
    assert r.status_code == 503
