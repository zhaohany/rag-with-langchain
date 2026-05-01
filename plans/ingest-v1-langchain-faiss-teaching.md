# Ingest V1 Teaching Plan (LangChain + Local HuggingFace + FAISS)

## 1) Goals

- Build a minimal, runnable ingest pipeline in `backend` for local docs.
- Keep architecture clean and extension-friendly for student exercises.
- Use local HuggingFace embeddings as default (no cloud dependency).
- Leave one clearly scoped student implementation function: chunking strategy enhancement.

## 2) Scope (What We Implement Now)

- `POST /api/v1/ingest` becomes functional (not 501).
- Ingest flow: discover docs -> read text -> chunk -> embed -> persist index + metadata -> update system status.
- Shared embedding module under `backend/app/shared/`.
- Baseline chunking implementation that is intentionally simple.
- Minimal tests proving end-to-end ingest works.

## 3) Out of Scope (For Later)

- Full query/RAG answer generation chain.
- Multi-provider embedding routing (OpenAI/vLLM) beyond interface hooks.
- Advanced chunking (semantic/token-aware) implementation.
- Heavy optimization (parallel ingest, retries, incremental indexing).

## 4) Reference Alignment

Primary reference: `/Users/zhaohanyan/Desktop/github/rag-chatbot/app`

- Follow the same high-level ingest orchestration style.
- Reuse similar data output structure (`faiss.index`, `metadata.json`, `system_meta.json`).
- Keep this repo simpler where possible.
- Key difference: prefer LangChain abstractions in embedding flow in this repo.

## 5) Target File Changes

- `backend/app/core/config.py`
  - Add ingest-related paths/settings:
    - `raw_docs_dir`
    - `index_path`
    - `metadata_path`
    - `embedding_model_name`
    - `embedding_batch_size`
    - `chunk_size`
    - `chunk_overlap`
- `backend/app/models/schemas.py`
  - Add `IngestResponse` schema.
- `backend/app/api/routes/ingest.py`
  - Replace not-implemented response with real service call.
  - Add structured error handling (`HTTPException(500, detail=...)`).
- `backend/app/services/ingest_service.py`
  - Implement ingest orchestration and status updates.
- `backend/app/shared/chunking.py` (new)
  - Baseline `split_into_chunks`.
  - Mark extension points for student exercise.
- `backend/app/shared/embedding.py` (new)
  - Local HF embedding model preload/get/embed abstraction via LangChain-compatible API.
- `backend/app/shared/ids.py` (new)
  - `make_doc_id`, `make_chunk_id`.
- `backend/tests/test_ingest_api.py` (new)
  - API-level ingest test.
- `backend/tests/test_chunking.py` (new)
  - Function-level chunking tests.
- `docs/api/endpoints-v1.md`
  - Update ingest contract from placeholder to implemented behavior.
- `AGENTS.md`
  - Add single-test commands and notes for ingest/chunking.

## 6) Architecture and Responsibilities

- Route layer (`api/routes/ingest.py`)
  - HTTP protocol only; no business logic.
- Service layer (`services/ingest_service.py`)
  - End-to-end ingest orchestration.
- Shared layer (`shared/*`)
  - Reusable low-level utilities (chunking, embedding, ids).
- Core config (`core/config.py`)
  - Runtime settings and data paths.

## 7) Data Contracts

### Ingest Response Payload

- `status: "success" | "failed"`
- `total_docs: int`
- `total_chunks: int`
- `message: str`

### Metadata Record (Per Chunk)

- `doc_id: str`
- `chunk_id: str`
- `source: str` (filename)
- `chunk_index: int`
- `chunk_text: str`

### System Status (`data/system/system_meta.json`)

- `ingestion_status: "idle" | "running" | "failed"`
- `last_success_ingestion_time: str | null` (ISO timestamp)
- `total_docs: int`

## 8) Baseline Ingest Flow (V1)

1. Set status to `running` (preserve last success timestamp/docs if exists).
2. Discover input docs from raw docs directory (markdown-first for simplicity).
3. Read each file as UTF-8.
4. Chunk with baseline splitter.
5. Embed chunk texts via local HF model wrapped in LangChain-compatible interface.
6. Persist FAISS index to `data/index/faiss.index`.
7. Persist metadata JSON to `data/meta/metadata.json`.
8. Update system meta to `idle` + new success timestamp + total docs.
9. Return summary payload.
10. On errors, set status to `failed` and raise clear runtime error.

## 9) Student Exercise Boundary (Single Function Focus)

Primary exercise function:

- `split_into_chunks(text, chunk_size, chunk_overlap) -> list[str]`

Baseline provided by instructors:

- Simple fixed-size overlapping character windows.

Enhancement tasks for students:

- Level 1: stronger validation and edge-case handling.
- Level 2: prefer paragraph/sentence boundaries before hard split.
- Level 3: token-aware chunking strategy with metadata support.

Acceptance criteria for student work:

- Deterministic chunk outputs.
- No empty chunks.
- Handles empty text and invalid params cleanly.
- Existing ingest pipeline remains compatible.

## 10) Embedding Strategy (Local HF Default)

- Keep embedding logic in `backend/app/shared/embedding.py`.
- Provide clean service-facing functions:
  - `preload_embedding_model()`
  - `get_embedding_model()`
  - `embed_texts(texts, batch_size)`
- Use local HuggingFace model by default.
- Keep abstraction provider-friendly so future OpenAI/vLLM support is additive.

## 11) Error Handling Rules

- Service catches file IO/parsing/model runtime exceptions and wraps actionable messages.
- Route converts service failures to `HTTP 500` with `detail`.
- Health endpoint behavior stays safe-default on malformed status file.
- Never leave system meta in ambiguous state; final status must be `idle` or `failed`.

## 12) Testing Plan

### Unit Tests

- `test_chunking.py`
  - empty input returns `[]`
  - overlap validation
  - deterministic chunk boundaries
  - no blank chunks

### API/Service Tests

- `test_ingest_api.py`
  - ingest success with sample docs
  - response field correctness
  - metadata/system files written
  - failure path sets status to `failed` (if feasible with controlled fault injection)

### Commands

- Single file: `pytest tests/test_ingest_api.py`
- Single test: `pytest tests/test_ingest_api.py::test_ingest_success`
- Chunking targeted: `pytest tests/test_chunking.py -k overlap`
- Full backend: `pytest`

## 13) Documentation Updates

- `docs/api/endpoints-v1.md`
  - Replace placeholder ingest section with real response shape and behavior.
- `AGENTS.md`
  - Add ingest/chunking test commands and extension notes for student exercise.

## 14) Implementation Sequence

1. Add config fields.
2. Add ingest response schema.
3. Create shared modules (`chunking`, `embedding`, `ids`).
4. Implement ingest service orchestration.
5. Wire ingest route.
6. Add tests.
7. Update docs.
8. Run backend tests and fix.

## 15) Definition of Done

- `POST /api/v1/ingest` runs successfully on local sample docs.
- FAISS index + metadata + system status are generated/updated correctly.
- New tests pass.
- API docs and AGENTS guidance are updated.
- Chunking exercise boundary is explicit and ready for students.
