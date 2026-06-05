from __future__ import annotations

import json

import pytest

from app.core.config import settings
from app.services.health_service import HealthService
from app.shared.chunking import split_markdown_chunks


def _example_slugify_title(title: str) -> str:
    return title.strip().lower().replace(" ", "-")


def _example_require_positive(value: int) -> int:
    if value <= 0:
        raise ValueError("value must be positive")
    return value


def test_example_plain_assertion() -> None:
    """Reference example: call a function and assert the exact return value."""
    result = _example_slugify_title("  Hello Pytest Class  ")

    assert result == "hello-pytest-class"


def test_example_pytest_raises() -> None:
    """Reference example: use pytest.raises for expected errors."""
    with pytest.raises(ValueError, match="value must be positive"):
        _example_require_positive(0)


def test_split_markdown_chunks_returns_empty_list_for_blank_text() -> None:
    """Scenario: blank markdown input should return an empty list."""
    text = "   \n\n  "
    chunk_size = 100
    chunk_overlap = 10

    pytest.fail("Student TODO: call split_markdown_chunks(...) and assert the result is []")


def test_split_markdown_chunks_rejects_invalid_chunk_settings() -> None:
    """Scenario: invalid chunk size or overlap values should raise ValueError."""
    text = "# Title\n\nShort body."
    invalid_settings = [
        {"chunk_size": 0, "chunk_overlap": 0},
        {"chunk_size": 100, "chunk_overlap": -1},
        {"chunk_size": 100, "chunk_overlap": 100},
    ]

    pytest.fail("Student TODO: loop through invalid_settings and assert each call raises ValueError")


def test_split_markdown_chunks_preserves_small_markdown_block() -> None:
    """Scenario: markdown shorter than chunk_size should be returned as one clean chunk."""
    text = "  # Course Notes\n\nThis is a short markdown document.  "
    chunk_size = 500
    chunk_overlap = 50
    expected_chunk = "# Course Notes\n\nThis is a short markdown document."

    pytest.fail("Student TODO: call split_markdown_chunks(...) and assert it returns [expected_chunk]")


def test_health_service_returns_defaults_when_meta_file_is_missing(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Scenario: missing system metadata file should produce safe default health values."""
    missing_meta_path = tmp_path / "missing-system-meta.json"
    monkeypatch.setattr(settings, "system_meta_path", missing_meta_path)
    service = HealthService()

    pytest.fail("Student TODO: call service.get_status() and assert the default health fields")


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

    pytest.fail("Student TODO: call service.get_status() and assert it reflects meta_payload")


def test_health_service_falls_back_when_system_metadata_is_invalid(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Scenario: invalid system metadata JSON should not crash and should return defaults."""
    meta_path = tmp_path / "broken-system-meta.json"
    meta_path.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(settings, "system_meta_path", meta_path)
    service = HealthService()

    pytest.fail("Student TODO: call service.get_status() and assert the default health fields")
