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

用途：触发本地文档 ingest 流程。

Request body: optional (V1 可以为空)

Behavior:

- Reads `*.md` files from `data/raw_docs/`
- Splits content into overlapping chunks
- Embeds chunks with local HuggingFace model
- Writes FAISS index to `data/index/faiss.index`
- Writes chunk metadata to `data/meta/metadata.json`
- Updates ingest status in `data/system/system_meta.json`

Failure:

- Returns `HTTP 500` with `detail` if ingest fails
- Sets `ingestion_status` to `failed` in system metadata

Response example:

```json
{
  "status": "success",
  "total_docs": 3,
  "total_chunks": 18,
  "message": "Ingestion completed"
}
```

## POST /api/v1/query

用途：执行检索增强问答。

Request example:

```json
{
  "question": "How do I reset my account password?",
  "session_id": "demo-local"
}
```

Response example:

```json
{
  "answer": "To reset your password, open the account portal and choose Reset Password.",
  "used_top_k": 4,
  "retrieved_chunks": [
    {
      "chunk_id": "doc_001_chunk_003",
      "doc_id": "doc_001",
      "score": 0.87,
      "text": "...",
      "source": "employee_handbook.md"
    }
  ]
}
```

## Optional (V1.1)

- `GET /api/v1/documents`
- `DELETE /api/v1/documents/{doc_id}`
