from __future__ import annotations


def make_doc_id(doc_index: int) -> str:
    if doc_index <= 0:
        raise ValueError("doc_index must be greater than 0")
    return f"doc_{doc_index}"


def make_chunk_id(doc_id: str, chunk_index: int) -> str:
    if not doc_id:
        raise ValueError("doc_id must not be empty")
    if chunk_index <= 0:
        raise ValueError("chunk_index must be greater than 0")
    return f"{doc_id}_chunk_{chunk_index}"
