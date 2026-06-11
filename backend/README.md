# Backend Skeleton

当前已包含可运行的 FastAPI backend：

- `GET /api/v1/health` 可用
- `POST /api/v1/ingest` 已实现（LangChain splitter + local HuggingFace embeddings + FAISS）
- `POST /api/v1/query` 已接入 answer generation 流程（Gemini client 调用留作业实现）

Query 课堂作业核心函数：

- `app/services/providers/gemini_client.py::GeminiClient.generate_content`
  - 输入：`prompt: str`
  - 输出：Gemini 返回的 `response.text`
  - 要求：
    - 用 `genai.Client(api_key=...)`
    - 调 `client.models.generate_content(...)`
    - 使用 `settings.gemini_model` 和 `settings.llm_max_output_tokens`
    - `response_mime_type="application/json"`
    - 将 SDK/API 异常转成 `GeminiClientError`

本地环境变量（学生本地自填）：

- `RAG_GEMINI_API_KEY=<your_key>`
- `RAG_GEMINI_MODEL=models/gemini-2.5-flash`（可选覆盖）
- `RAG_LLM_MAX_OUTPUT_TOKENS=256`（可选覆盖）

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
