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
