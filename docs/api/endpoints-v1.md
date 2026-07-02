# API Contract (V1)

Base URL: `http://127.0.0.1:8000`

说明：V1 仅定义契约和返回结构，优先保证链路清晰。

## GET /api/v1/health

用途：服务健康检查和 ingest 状态读取。

Response example:

```json
{
  "status": "ok",
  "version": "0.1.0",
  "environment": "local",
  "ingestion_status": "idle",
  "last_success_ingestion_time": null,
  "total_docs": 0
}
```

## POST /api/v1/ingest

用途：提交一个本地 ingest job。API 会立刻返回 `queued`，实际 embedding / FAISS / SQLite 写入由 FastAPI `BackgroundTasks` 在 response 返回后继续执行。

说明：这不是定时任务，也不是 Redis/Celery 分布式队列。一次 `/ingest` 请求对应一个 job，这个 job 会处理所有 `raw_docs/*.md` 并全量重建本地索引。

Request body: optional (V1 可以为空)

Behavior:

- Reads `*.md` files from `data/raw_docs/`
- Splits content into overlapping chunks
- Embeds chunks with local HuggingFace model
- Writes FAISS index to `data/index/faiss.index`
- Writes chunk metadata to SQLite at `data/meta/rag.sqlite3`
- Updates ingest status in SQLite at `data/meta/rag.sqlite3`

Failure:

- Returns `HTTP 409` with `detail` if another ingest job is already queued or running
- Returns `HTTP 500` with `detail` if ingest fails
- Sets `ingestion_status` to `failed` in SQLite system metadata

Response example:

```json
{
  "status": "queued",
  "total_docs": 0,
  "total_chunks": 0,
  "message": "Ingestion job submitted",
  "job_id": "ingest_20260628_123456_000000"
}
```

Use `GET /api/v1/health` to observe app-level ingestion status:

```text
queued -> running -> idle
queued -> running -> failed
```

## POST /api/v1/query

用途：执行检索并返回相关文档片段（V1 skeleton 不生成答案）。

Request example:

```json
{
  "question": "How do I reset my account password?",
  "session_id": "demo-local"
}
```

Behavior (current skeleton):

- Loads local FAISS index from `data/index/`
- Embeds `question` with local HuggingFace model
- Retrieves top-k chunks (default `k=1`)
- Builds final query prompt from template and retrieved context, then writes to `data/prompts/final_prompt.txt`
- Returns retrieved chunks only (no `answer` field yet)

Response example:

```json
{
  "used_top_k": 1,
  "retrieved_chunks": [
    {
      "chunk_id": "doc_1_chunk_3",
      "doc_id": "doc_1",
      "score": 0.2451,
      "text": "### Password Reset ...",
      "source": "company_it_support_playbook.md"
    }
  ]
}
```

## Optional (V1.1)

- `GET /api/v1/documents`
- `DELETE /api/v1/documents/{doc_id}`
