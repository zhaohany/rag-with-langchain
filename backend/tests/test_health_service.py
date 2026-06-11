from __future__ import annotations

import sqlite3

import pytest

from app.core.config import settings
from app.services.health_service import HealthService


def test_health_service_returns_defaults_when_meta_file_is_missing(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Scenario: missing system metadata file should produce safe default health values."""
    monkeypatch.setattr(settings, "database_path", tmp_path / "missing.sqlite3")
    service = HealthService()

    status = service.get_status()

    assert status["ingestion_status"] == "idle"
    assert status["last_success_ingestion_time"] is None
    assert status["total_docs"] == 0


def test_health_service_reads_valid_system_metadata(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Scenario: valid SQLite system metadata should be reflected in health status."""
    database_path = tmp_path / "rag.sqlite3"
    meta_payload = {
        "ingestion_status": "running",
        "last_success_ingestion_time": "2026-06-04T12:00:00Z",
        "total_docs": 7,
    }
    monkeypatch.setattr(settings, "database_path", database_path)
    with sqlite3.connect(database_path) as conn:
        conn.execute(
            """
            CREATE TABLE system_meta (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                ingestion_status TEXT NOT NULL,
                last_success_ingestion_time TEXT,
                total_docs INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            INSERT INTO system_meta (id, ingestion_status, last_success_ingestion_time, total_docs)
            VALUES (1, ?, ?, ?)
            """,
            (
                meta_payload["ingestion_status"],
                meta_payload["last_success_ingestion_time"],
                meta_payload["total_docs"],
            ),
        )
    service = HealthService()

    status = service.get_status()

    assert status["ingestion_status"] == meta_payload["ingestion_status"]
    assert status["last_success_ingestion_time"] == meta_payload["last_success_ingestion_time"]
    assert status["total_docs"] == meta_payload["total_docs"]


def test_health_service_falls_back_when_system_metadata_is_invalid(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Scenario: invalid SQLite system metadata should not crash and should return defaults."""
    database_path = tmp_path / "broken.sqlite3"
    database_path.write_text("not a sqlite database", encoding="utf-8")
    monkeypatch.setattr(settings, "database_path", database_path)
    service = HealthService()

    status = service.get_status()

    assert status["ingestion_status"] == "idle"
    assert status["last_success_ingestion_time"] is None
    assert status["total_docs"] == 0
