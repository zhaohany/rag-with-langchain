# Setup on Windows

## 1) Backend (PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

Swagger: `http://127.0.0.1:8000/docs`

Backend (CMD) 版本：

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 2) Backend tests (PowerShell)

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

Backend tests (CMD) 版本：

```bat
cd backend
.venv\Scripts\activate.bat
pytest
```

## 3) Frontend UI (PowerShell)

```powershell
cd frontend
copy .env.example .env
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`

Frontend UI (CMD) 版本：

```bat
cd frontend
copy .env.example .env
npm install
npm run dev
```

## 4) Quick verify

- UI 页面加载后会自动调用 `GET /api/v1/health`
- 如需手动重试，可点击顶部 `Health: ...` 状态按钮
- 或直接请求 `GET /api/v1/health`
