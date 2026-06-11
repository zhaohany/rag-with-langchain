from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Union

from langchain_core.runnables import RunnableLambda
from langchain_community.vectorstores import FAISS

from app.core.config import settings
from app.services.database_store import database_store
from app.shared.chunking import split_markdown_chunks
from app.shared.embedding import get_embedding_model
from app.shared.ids import make_chunk_id, make_doc_id


def discover_markdown_files(raw_docs_dir: Path) -> list[Path]:
    if not raw_docs_dir.exists():
        return []
    return sorted(path for path in raw_docs_dir.glob("*.md") if path.is_file())


def write_faiss_index(chunk_texts: list[str], metadatas: list[dict[str, Any]], index_path: Path) -> None:
    if len(chunk_texts) != len(metadatas):
        raise ValueError("texts and metadata length mismatch")

    store = FAISS.from_texts(
        texts=chunk_texts,
        embedding=get_embedding_model(),
        metadatas=metadatas,
    )
    index_path.parent.mkdir(parents=True, exist_ok=True)
    store.save_local(str(index_path.parent), index_name=index_path.stem)


def remove_faiss_index(index_path: Path) -> None:
    base = index_path.parent / index_path.stem
    for suffix in (".faiss", ".pkl"):
        candidate = Path(f"{base}{suffix}")
        if candidate.exists():
            candidate.unlink()


class IngestService:
    def _set_status(self, ingestion_status: str, previous_meta: dict[str, Union[str, int, None]]) -> None:
        self._write_system_meta({**previous_meta, "ingestion_status": ingestion_status})

    def _step_discover(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload["docs"] = discover_markdown_files(settings.raw_docs_dir)
        return payload

    def _step_chunk(self, payload: dict[str, Any]) -> dict[str, Any]:
        docs: list[Path] = payload["docs"]
        records: list[dict[str, Any]] = []
        chunk_texts: list[str] = []

        for file_index, doc_path in enumerate(docs, start=1):
            doc_id = make_doc_id(file_index)
            text = doc_path.read_text(encoding="utf-8")
            chunks = split_markdown_chunks(text, settings.chunk_size, settings.chunk_overlap)
            for chunk_index, chunk_text in enumerate(chunks, start=1):
                records.append(
                    {
                        "doc_id": doc_id,
                        "chunk_id": make_chunk_id(doc_id, chunk_index),
                        "source": doc_path.name,
                        "chunk_index": chunk_index,
                        "chunk_text": chunk_text,
                    }
                )
                chunk_texts.append(chunk_text)

        payload["records"] = records
        payload["chunk_texts"] = chunk_texts
        return payload

    def _step_embed_and_persist(self, payload: dict[str, Any]) -> dict[str, Any]:
        chunk_texts: list[str] = payload["chunk_texts"]
        if chunk_texts:
            records: list[dict[str, Any]] = payload["records"]
            metadatas = [
                {
                    "doc_id": record["doc_id"],
                    "chunk_id": record["chunk_id"],
                    "source": record["source"],
                    "chunk_index": record["chunk_index"],
                }
                for record in records
            ]
            write_faiss_index(chunk_texts, metadatas, settings.index_path)
        else:
            remove_faiss_index(settings.index_path)

        database_store.replace_chunk_metadata(payload["records"])
        return payload

    def run_sync_ingest(self) -> dict[str, Any]:
        previous_meta = self._read_system_meta()
        self._set_status("running", previous_meta)

        try:
            chain = (
                RunnableLambda(self._step_discover)
                | RunnableLambda(self._step_chunk)
                | RunnableLambda(self._step_embed_and_persist)
            )
            result = chain.invoke({})
            docs: list[Path] = result["docs"]
            records: list[dict[str, Any]] = result["records"]

            finished_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            total_docs = len(docs)
            self._write_system_meta(
                {
                    "ingestion_status": "idle",
                    "last_success_ingestion_time": finished_at,
                    "total_docs": total_docs,
                }
            )

            return {"status": "success", "total_docs": total_docs, "total_chunks": len(records), "message": "Ingestion completed"}
        except (OSError, ValueError, RuntimeError, sqlite3.DatabaseError) as exc:
            self._set_status("failed", previous_meta)
            raise RuntimeError(f"Ingestion failed: {exc}") from exc

    def _read_system_meta(self) -> dict[str, Union[str, int, None]]:
        return database_store.get_system_meta()

    def _write_system_meta(self, payload: dict[str, Union[str, int, None]]) -> None:
        database_store.write_system_meta(payload)


ingest_service = IngestService()
