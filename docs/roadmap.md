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

- 容器化部署
- 数据目录与模型依赖管理
- 云环境配置与服务暴露

## Milestone 7: DB Enhancement

- 从静态 JSON metadata 迁移到 SQLite
- 设计 documents、chunks、ingest_runs、query_runs、sources 等核心表
- 保留 FAISS 作为向量索引产物，SQLite 管理结构化状态与审计信息
- 增加初始化或迁移脚本

## Milestone 8: Docker 化

- 后端 Dockerfile
- 前端 Dockerfile 或静态构建镜像
- `docker-compose.yml` 编排 backend、frontend 与本地 data volume
- 明确 index/meta/system 等运行产物的挂载策略

## Milestone 9: Document Source 扩展

- 支持从 online docs ingest
- 支持 URL source 配置与正文抽取
- 复用现有 chunking、embedding、FAISS index 流程
- 在 metadata 中记录 source type、source URL、fetch time 等溯源信息

## Milestone 10: Evals

- 准备 golden questions / expected sources 数据集
- 评估 retrieval hit rate、MRR、source overlap 等指标
- 接入 LLM answer 后评估 faithfulness、groundedness、引用正确性
- 后续与 MLflow 实验跟踪结合
