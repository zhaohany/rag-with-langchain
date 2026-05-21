from __future__ import annotations

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


def split_markdown_chunks(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    normalized = text.strip()
    if not normalized:
        return []

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")],
        strip_headers=False,
    )
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks: list[str] = []
    for header_doc in header_splitter.split_text(normalized):
        block = header_doc.page_content.strip()
        if not block:
            continue

        if len(block) <= chunk_size:
            chunks.append(block)
            continue

        for fragment in recursive_splitter.split_text(block):
            candidate = fragment.strip()
            if candidate:
                chunks.append(candidate)

    return chunks
