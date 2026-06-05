from __future__ import annotations

import pytest


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
