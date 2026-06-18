# 项目当前整体状态（持续更新）

更新时间：2026-06-04

## 功能完成度

- health：可用
- ingest：可用（discover + recursive chunking + embedding + FAISS index + SQLite metadata/system 状态落盘）
- query：可用（retrieval + prompt 组装与落盘），但仍未接入 LLM 生成最终答案

---

## 具体完成了什么

### 后端 API 与基础设施

- FastAPI 应用、CORS、版本化路由已就位：`backend/app/main.py`
- 路由分层清晰：`backend/app/api/routes/health.py`、`backend/app/api/routes/ingest.py`、`backend/app/api/routes/query.py`

### Health（已可用于状态观测）

- `GET /api/v1/health` 返回服务状态、环境、版本、ingest 状态、最后成功时间、文档数
- 会读取 SQLite system metadata，读取失败时回退默认值
- 实现位置：`backend/app/services/health_service.py`

### Ingest（已是完整可执行链路）

- `POST /api/v1/ingest` 会实际执行流程并返回汇总结果（非占位）
- 流程包括：
  - 扫描 `data/raw_docs/*.md`
  - 按 Markdown 标题 + RecursiveCharacterTextSplitter 分块
  - 使用本地 embedding 模型向量化
  - 写入本地 FAISS 索引
  - 写入 SQLite metadata 与 system meta
- 关键实现：`backend/app/services/ingest_service.py`、`backend/app/shared/chunking.py`

### Query（已完成检索主链路，未完成答案生成）

- `POST /api/v1/query` 已接线到 `QueryService.run_query(...)`，非 501 占位
- 当前已实现：
  - 输入问题校验
  - 加载本地 FAISS
  - 相似度检索 top-k
  - 组装 `retrieved_chunks` 返回
  - 根据模板构建并落盘最终 prompt 到 `data/prompts/final_prompt.txt`
- 关键实现：`backend/app/services/query_service.py`、`backend/app/services/prompt_service.py`

### Frontend（基础可用）

- 已有可运行聊天页 + 健康状态面板：`frontend/src/App.tsx`
- 已接后端 health/query API：`frontend/src/api/rag.ts`
- 当前前端对 query 结果以兜底文本展示（若无 `answer` 字段则展示返回 JSON）

### 本地数据产物（流程运行证据）

- `data/index/faiss.faiss`
- `data/index/faiss.pkl`
- `data/meta/rag.sqlite3`

---

## 当前未完成/主要缺口

- 未完成真正的 Answer Generation（LLM integration）
- Query 目前停在“检索 + prompt 构建”，尚未返回高质量自然语言答案
- prompt 模板与上下文格式仍偏教学/样例形态，尚未做产品化优化
- `docs/api/endpoints-v1.md` 已更新为当前 query 行为：返回 `retrieved_chunks`，暂不返回 `answer`

---

## 按 Roadmap 的阶段进度

- Milestone 0（Project Foundation）：完成
- Milestone 1（Backend Skeleton）：完成
- Milestone 2（Ingestion Pipeline）：完成
- Milestone 3（Query Pipeline）：部分完成
  - 已完成：向量检索 top-k、sources 返回、prompt 组装
  - 未完成：回答生成（LLM）
- Milestone 4（Frontend Demo UI）：部分完成（基础 UI + API 接线已完成）
- Milestone 5（Future Extension）：未开始
- Milestone 6（Production 部署和云服务）：未开始

---

## 设想中的新增 Roadmaps

### DB Enhancement：从静态文件迁移到 SQLite

- 当前状态：部分完成
- 目标：将 metadata、ingest/query 运行记录、文档源信息等从静态 JSON 文件逐步迁移到 SQLite 实例
- 初步范围：
  - 已完成：保留 FAISS index 文件作为向量索引产物，SQLite 负责 chunk metadata 与 ingest 状态
  - 待完成：扩展 SQLite schema（documents、ingest_runs、query_runs、sources）
  - 待完成：为 query 运行记录提供更稳定的审计能力

### Docker 化

- 当前状态：未开始
- 目标：提供可复现的本地启动方式，降低环境配置成本
- 初步范围：
  - 后端 Dockerfile（FastAPI + Python dependencies）
  - 前端 Dockerfile 或静态构建镜像
  - `docker-compose.yml` 编排 backend、frontend，以及未来 SQLite volume/data volume
  - 明确本地数据目录挂载策略，避免 index/meta/system 数据丢失

### Document Source：支持在线文档 ingest

- 当前状态：未开始
- 目标：从仅支持 `data/raw_docs/*.md` 扩展到可 ingest online docs
- 初步范围：
  - 支持 URL source 配置（单页 URL、站点文档入口、后续可扩展 sitemap）
  - 抓取 HTML/Markdown 后抽取正文、标题、链接、更新时间等 metadata
  - 与现有 chunking/embedding/index 流程复用
  - 在 metadata 中记录 source type、source URL、fetch time，便于溯源和重新 ingest

### Evals：检索与回答质量评估

- 当前状态：未开始
- 目标：建立基础评估闭环，量化 retrieval 和后续 answer generation 的质量
- 初步范围：
  - 准备小规模 golden questions / expected sources 数据集
  - 评估 retrieval hit rate、MRR、source overlap 等指标
  - 接入 LLM answer 后增加 answer faithfulness、context groundedness、引用正确性检查
  - 后续可与 MLflow roadmap 结合，记录不同 chunking/embedding/top-k 配置的实验结果

---

## 下次更新建议

每次更新本文件时，至少同步以下事项：

- query 是否已接入 LLM 并返回 `answer`
- docs 契约是否与代码保持一致
- frontend 展示是否从 JSON 兜底升级为答案 + sources 结构化展示
- 关键数据产物与健康状态是否正常
- 新增 roadmaps 是否已拆成可执行 milestone，并同步到 `docs/roadmap.md`
