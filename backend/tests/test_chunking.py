from __future__ import annotations

from app.shared.chunking import split_markdown_chunks


def test_split_markdown_chunks_returns_empty_list_for_blank_text() -> None:
    """Scenario: blank markdown input should return an empty list."""
    text = "   \n\n  "
    chunk_size = 100
    chunk_overlap = 10

    result = split_markdown_chunks(text, chunk_size, chunk_overlap)

    assert result == []


def test_split_markdown_chunks_rejects_invalid_chunk_settings() -> None:
    """Scenario: invalid chunk size or overlap values should raise ValueError."""
    text = "# Title\n\nShort body."
    invalid_settings = [
        {"chunk_size": 0, "chunk_overlap": 0},
        {"chunk_size": 100, "chunk_overlap": -1},
        {"chunk_size": 100, "chunk_overlap": 100},
    ]

    for settings in invalid_settings:
        try:
            split_markdown_chunks(text, settings["chunk_size"], settings["chunk_overlap"])
            assert False, f"Expected ValueError for {settings}"
        except ValueError:
            pass


def test_split_markdown_chunks_preserves_small_markdown_block() -> None:
    """Scenario: markdown shorter than chunk_size should be returned as one clean chunk."""
    text = "  # Course Notes\n\nThis is a short markdown document.  "
    chunk_size = 500
    chunk_overlap = 50
    expected_chunk = "# Course Notes  \nThis is a short markdown document."

    result = split_markdown_chunks(text, chunk_size, chunk_overlap)

    assert result == [expected_chunk]
