# Frontend Skeleton

当前已包含可运行的 React + Vite skeleton：

- 聊天界面风格参考 `rag-chatbot` 示例（简洁布局）
- 启动时自动检查 `GET /api/v1/health`
- 可发送问题到 `POST /api/v1/query`（当前后端会返回 not implemented）

## Run

```bash
npm install
npm run dev
```

默认地址：`http://127.0.0.1:5173`

```text
frontend/
  src/
    main.tsx
    App.tsx
    api/
      client.ts
      rag.ts
    types/
      api.ts
```
