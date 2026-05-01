from __future__ import annotations


def split_into_chunks(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    normalized = text.strip()
    if not normalized:
        return []

    chunks: list[str] = []
    step = chunk_size - chunk_overlap
    start = 0
    while start < len(normalized):
        end = start + chunk_size
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks


def split_into_recursive_chunks(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Homework function: implement recursive structure-aware chunking.

    Input/Output contract (must match `split_into_chunks`):
    - Input:
      - `text`: original markdown text
      - `chunk_size`: max characters for each output chunk
      - `chunk_overlap`: overlap characters for fallback splitting
    - Output:
      - `list[str]`: ordered chunk texts, ready for downstream embedding

    This function should be a drop-in replacement for `split_into_chunks` in ingest
    after students finish implementation.

    Required behavior:
    1) Validate arguments with the same rules as `split_into_chunks`:
       - `chunk_size > 0`
       - `chunk_overlap >= 0`
       - `chunk_overlap < chunk_size`
    2) Normalize input (`text.strip()`). If empty, return `[]`.
    3) Recursive splitting strategy:
       - First split by H2 headers (`## `) into sections.
       - If an H2 section length is `<= chunk_size`, keep it as one chunk.
       - If an H2 section is too long, split that section by H3 headers (`### `).
       - For each H3 part:
         - keep directly if `<= chunk_size`
         - if still too long, fallback to naive `split_into_chunks(...)`
           using the same `chunk_size` and `chunk_overlap`.
       - If an oversized H2 section has no valid H3 boundaries,
         fallback directly to naive `split_into_chunks(...)`.
    4) Preserve original document order in final output.
    5) Never return empty/blank chunks.
    6) Output must be deterministic: same input -> same output.

    Suggested helper breakdown (optional):
    - `_split_sections_by_header(text: str, header_prefix: str) -> list[str]`
    - `_append_non_empty(chunks: list[str], candidate: str) -> None`

    Example 1 (H2 fits directly):
    - Input:
      text = "## VPN Access\nUse company VPN before internal tools."
      chunk_size = 120, chunk_overlap = 20
    - Expected output:
      ["## VPN Access\nUse company VPN before internal tools."]

    Example 2 (H2 too long, H3 split works):
    - Input:
      text = (
        "## Network Troubleshooting\n"
        "<long intro ...>\n"
        "### DNS Checks\n...\n"
        "### Proxy Checks\n..."
      )
      chunk_size = 300, chunk_overlap = 40
    - Expected output:
      - multiple chunks aligned to H3 parts (in order),
      - each chunk ideally `<= chunk_size` unless fallback is needed.

    Example 3 (H3 still too long -> fallback naive split):
    - Input:
      text = "## Incident Report\n### Full Timeline\n" + "A" * 2000
      chunk_size = 500, chunk_overlap = 50
    - Expected output:
      - timeline part split into overlapping windows via `split_into_chunks`.
    """
    raise NotImplementedError("Homework: implement recursive structure-aware chunking")
