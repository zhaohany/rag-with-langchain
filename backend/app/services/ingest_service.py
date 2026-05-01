from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from typing import Any

from langchain_core.runnables import RunnableLambda
from langchain_community.vectorstores import FAISS

from app.core.config import settings
from app.shared.chunking import split_into_chunks
from app.shared.embedding import embed_texts
from app.shared.ids import make_chunk_id, make_doc_id


def discover_markdown_files(raw_docs_dir: Path) -> list[Path]:
    if not raw_docs_dir.exists():
        return []
    return sorted(path for path in raw_docs_dir.glob("*.md") if path.is_file())


def write_faiss_index(chunk_texts: list[str], vectors: np.ndarray, index_path: Path) -> None:
    if vectors.ndim != 2:
        raise ValueError("vectors must be 2-dimensional")
    if len(chunk_texts) != int(vectors.shape[0]):
        raise ValueError("texts and vectors length mismatch")

    pair_values = list(zip(chunk_texts, vectors.tolist(), strict=True))
    store = FAISS.from_embeddings(
        text_embeddings=pair_values,
        embedding=None,  # type: ignore[arg-type]
        metadatas=[{} for _ in chunk_texts],
    )
    index_path.parent.mkdir(parents=True, exist_ok=True)
    store.save_local(str(index_path.parent), index_name=index_path.stem)


def write_metadata(records: list[dict[str, Any]], metadata_path: Path) -> None:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


class IngestService:
    def _set_status(self, ingestion_status: str, previous_meta: dict[str, str | int | None]) -> None:
        self._write_system_meta({"ingestion_status": ingestion_status, **previous_meta})

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
            # Homework hook: replace with split_into_recursive_chunks after student implementation.
            chunks = split_into_chunks(text, settings.chunk_size, settings.chunk_overlap)
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
            vectors = np.asarray(embed_texts(chunk_texts, settings.embedding_batch_size), dtype=np.float32)
            write_faiss_index(chunk_texts, vectors, settings.index_path)
        elif settings.index_path.exists():
            settings.index_path.unlink()

        write_metadata(payload["records"], settings.metadata_path)
        return payload

    def _step_finalize(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Homework function: move finalize logic into the LangChain chain.

        Current production path keeps finalize outside the chain so MVP stays runnable.
        Students can implement this as an optional enhancement and then append it to:
        discover -> chunk -> embed_and_persist -> finalize.

        Input payload contract:
        - `payload["docs"]`: list[Path]
        - `payload["records"]`: list[dict[str, Any]]

        Required behavior:
        1) Compute `total_docs` from docs and `total_chunks` from records.
        2) Write system metadata with:
           - ingestion_status = "idle"
           - last_success_ingestion_time = current UTC ISO string with trailing Z
           - total_docs
        3) Add `payload["response"]` with fields:
           - status: "success"
           - total_docs: int
           - total_chunks: int
           - message: "Ingestion completed"
        4) Return updated payload.

        Note:
        - Do not break current default flow; this step is optional until wired in.
        - Homework hook (where to change):
          1) In `run_sync_ingest`, append `RunnableLambda(self._step_finalize)` to the chain.
          2) Then return `result["response"]` from chain output instead of building response outside chain.
        """
        raise NotImplementedError("Homework: implement finalize chain step")

    def run_sync_ingest(self) -> dict[str, Any]:
        previous_meta = self._read_system_meta()
        self._set_status("running", previous_meta)

        try:
            # Homework hook: after implementing `_step_finalize`, append it as final chain step.
            chain = (
                RunnableLambda(self._step_discover)
                | RunnableLambda(self._step_chunk)
                | RunnableLambda(self._step_embed_and_persist)
                # | RunnableLambda(self._step_finalize)
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
        except (OSError, ValueError, RuntimeError) as exc:
            self._set_status("failed", previous_meta)
            raise RuntimeError(f"Ingestion failed: {exc}") from exc

    def _read_system_meta(self) -> dict[str, str | int | None]:
        if not settings.system_meta_path.exists():
            return {"last_success_ingestion_time": None, "total_docs": 0}

        try:
            raw = json.loads(settings.system_meta_path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise ValueError("Invalid system meta format")
            return {
                "last_success_ingestion_time": raw.get("last_success_ingestion_time"),
                "total_docs": int(raw.get("total_docs") or 0),
            }
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return {"last_success_ingestion_time": None, "total_docs": 0}

    def _write_system_meta(self, payload: dict[str, str | int | None]) -> None:
        settings.system_meta_path.parent.mkdir(parents=True, exist_ok=True)
        settings.system_meta_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


ingest_service = IngestService()
