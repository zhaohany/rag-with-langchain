# Setup on macOS

## 1) Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

Swagger: `http://127.0.0.1:8000/docs`

## 2) Backend tests

```bash
cd backend
source .venv/bin/activate
pytest
```

## 3) Frontend UI

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`

## 4) Quick verify

- UI 页面加载后会自动调用 `GET /api/v1/health`
- 如需手动重试，可点击顶部 `Health: ...` 状态按钮
- 或直接请求 `GET /api/v1/health`
