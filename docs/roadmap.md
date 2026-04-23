# Roadmap (Local First)

## Milestone 0: Project Foundation

- 完成目录结构初始化
- 明确 V1 API 契约
- 完成架构与实施文档

## Milestone 1: Backend Skeleton

- FastAPI app 与路由骨架
- `health` / `ingest` / `query` 的 schema 和 service skeleton
- 基础配置与日志框架

## Milestone 2: Ingestion Pipeline

- 文档发现与读取
- chunking 与 embedding
- 向量索引和 metadata 持久化

## Milestone 3: Query Pipeline

- 向量检索 top-k
- prompt 组装和回答生成
- 返回 sources 引用信息

## Milestone 4: Frontend Demo UI

- 极简 chat 页面
- 连接后端 query API
- 展示答案和 source 片段

## Milestone 5: Future Extension

- 接入 MLflow 做实验跟踪
- 接入 vLLM 作为模型服务后端

## Milestone 6: Production部署和云服务
