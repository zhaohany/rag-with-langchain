# Local Architecture (V1)

## 目标

- 快速完成本地可运行的 RAG 闭环
- 保持代码分层清晰，便于维护
- 为后续 MLflow / vLLM 预留扩展边界

## 系统组成

- `backend/`: FastAPI + LangChain（API 和 RAG 核心逻辑）
- `frontend/`: React 小型聊天 UI（联调和展示）
- `data/`: 本地文档、索引、元数据
- `docs/`: 架构、接口、setup、roadmap
- `mlops/`: 后续实验与模型服务接入预留

## 后端分层约定

- `api/routes`: HTTP 路由层，只做协议转换
- `models`: 请求响应 Schema
- `services`: 业务流程编排（ingest/query）
- `shared`: 复用工具（chunking、prompts、ids）
- `core`: 配置、日志、应用级基础能力

## V1 数据流

1. `POST /api/v1/ingest`
   - 读取本地文档
   - 文本切分
   - embedding
   - 写入向量索引和 metadata

2. `POST /api/v1/query`
   - 接收用户问题
   - 向量检索 top-k
   - 组装上下文和 prompt
   - 生成答案并返回 sources

3. `GET /api/v1/health`
   - 返回服务状态与 ingest 元信息

## 扩展策略

- 模型后端通过 provider 抽象替换（local/openai/vllm）
- API 契约稳定，替换底层实现不影响前端
- 评估与实验数据写入 `mlops/`，避免污染业务代码
