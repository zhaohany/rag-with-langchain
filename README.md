# RAG with LangChain (Local First)

这个项目用于搭建一个本地可运行的 RAG 系统。

当前阶段聚焦三件事：

- FastAPI API 骨架（health / ingest / query）
- LangChain 依赖和扩展位先准备好
- React 极简聊天 UI（用于联调和演示）

## V1 范围（本地）

- 仅本地运行，不上云，不引入复杂部署
- 先只实现 health，ingest/query 先保留占位 API
- 代码结构先设计清晰，便于后续接入 MLflow / vLLM

## Data 目录说明

- `data/raw_docs/`: 原始文档输入目录
- `data/index/`: 向量索引落盘目录（后续 ingest 使用）
- `data/meta/metadata.json`: chunk 元数据文件（后续 ingest 使用）
- `data/system/system_meta.json`: 系统状态文件（health API 会读取）

## 目录结构

```text
.
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── shared/
│   └── tests/
├── frontend/
│   └── src/
├── data/
│   ├── raw_docs/
│   ├── index/
│   ├── meta/
│   └── system/
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── setup/
│   └── roadmap.md
├── mlops/
│   ├── eval/
│   ├── mlflow/
│   └── vllm/
└── plans/
```

## 核心文档

- 架构说明：`docs/architecture/local.md`
- API 契约：`docs/api/endpoints-v1.md`
- 项目路线图：`docs/roadmap.md`

## Quick Start

后端：

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

后端测试：

```bash
cd backend
source .venv/bin/activate
pytest
```

前端：

```bash
cd frontend
npm install
npm run dev
```

完整 setup 文档：

- macOS: `docs/setup/mac.md`
- Windows (PowerShell): `docs/setup/windows.md`
