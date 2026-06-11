from __future__ import annotations

import json

import pytest

from app.core.config import settings
from app.services.health_service import HealthService


def test_health_service_returns_defaults_when_meta_file_is_missing(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Scenario: missing system metadata file should produce safe default health values."""
    missing_meta_path = tmp_path / "missing-system-meta.json"
    monkeypatch.setattr(settings, "system_meta_path", missing_meta_path)
    service = HealthService()

    pytest.fail("Exercise TODO: call service.get_status() and assert the default health fields")


def test_health_service_reads_valid_system_metadata(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Scenario: valid system metadata JSON should be reflected in health status."""
    meta_path = tmp_path / "system_meta.json"
    meta_payload = {
        "ingestion_status": "running",
        "last_success_ingestion_time": "2026-06-04T12:00:00Z",
        "total_docs": 7,
    }
    meta_path.write_text(json.dumps(meta_payload), encoding="utf-8")
    monkeypatch.setattr(settings, "system_meta_path", meta_path)
    service = HealthService()

    pytest.fail("Exercise TODO: call service.get_status() and assert it reflects meta_payload")


def test_health_service_falls_back_when_system_metadata_is_invalid(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Scenario: invalid system metadata JSON should not crash and should return defaults."""
    meta_path = tmp_path / "broken-system-meta.json"
    meta_path.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(settings, "system_meta_path", meta_path)
    service = HealthService()

    pytest.fail("Exercise TODO: call service.get_status() and assert the default health fields")
