# Backend Skeleton

当前已包含可运行的 FastAPI backend：

- `GET /api/v1/health` 可用
- `POST /api/v1/ingest` 已实现（LangChain splitter + local HuggingFace embeddings + FAISS）
- `POST /api/v1/query` 已实现 retrieval skeleton（返回检索文档，不生成答案）

Query 课堂作业核心函数：

- `app/services/query_service.py::_build_retrieved_chunk`
  - 输入：`text`, `metadata`, `raw_score`
  - 输出：`chunk_id/doc_id/score/text/source`
  - 要求：类型安全、缺失字段兜底、输出稳定可序列化

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
uvicorn app.main:app --reload
```

## Test

```bash
source .venv/bin/activate
pytest
```

Swagger: `http://127.0.0.1:8000/docs`

```text
backend/
  app/
    main.py
    api/routes/
      health.py
      ingest.py
      query.py
    core/
      config.py
      logging.py
    models/
      schemas.py
    services/
      health_service.py
      ingest_service.py
      query_service.py
  tests/
    test_health_api.py
```
