from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def test_health_endpoint_returns_expected_payload() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["version"] == settings.app_version
    assert payload["environment"] == settings.env
    assert payload["ingestion_status"] == "idle"
    assert payload["last_success_ingestion_time"] is None
    assert payload["total_docs"] == 0
