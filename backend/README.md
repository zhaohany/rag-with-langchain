# Backend Skeleton

当前已包含可运行的 FastAPI skeleton：

- `GET /api/v1/health` 可用
- `POST /api/v1/ingest` 预留（not implemented）
- `POST /api/v1/query` 预留（not implemented）

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
