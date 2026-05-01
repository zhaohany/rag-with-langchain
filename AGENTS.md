# AGENTS.md

This file provides repository-specific instructions for coding agents working in `rag-with-langchain`.

## Project Layout

- `backend/`: FastAPI service and Python tests.
- `frontend/`: React + TypeScript + Vite UI.
- `data/`: local runtime data (`raw_docs`, `index`, `meta`, `system`).
- `docs/`: architecture, API contracts, setup docs.
- `mlops/`: placeholders for eval/MLflow/vLLM integrations.

## External Agent Rules

- Cursor rules: none found (`.cursor/rules/` and `.cursorrules` do not exist).
- Copilot rules: none found (`.github/copilot-instructions.md` does not exist).
- If these files are added later, treat them as higher-priority repository policy and update this document.

## Environment Assumptions

- Backend is Python (venv-based local setup).
- Frontend is Node + npm.
- Default local API URL is `http://127.0.0.1:8000/api/v1`.
- Frontend dev server runs on `http://127.0.0.1:5173`.

## Build, Run, Lint, Test Commands

### Backend (`backend/`)

Setup and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run all tests:

```bash
source .venv/bin/activate
pytest
```

Run a single test file:

```bash
source .venv/bin/activate
pytest tests/test_health_api.py
```

Run a single test function:

```bash
source .venv/bin/activate
pytest tests/test_health_api.py::test_health_endpoint_returns_expected_payload
```

Useful targeted test pattern:

```bash
source .venv/bin/activate
pytest -k health
```


### Frontend (`frontend/`)

Install and run dev server:

```bash
npm install
npm run dev
```

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

Type-checking behavior:

- `npm run build` runs `tsc -b` before `vite build`.
- There is no dedicated `lint` script currently.
- There is no frontend test runner configured currently (no Vitest/Jest script).

### Repo Root

- No root-level unified build/test/lint script is defined.
- Run backend and frontend commands from their own directories.

## Coding Conventions (Observed + Enforced-by-Config)

Follow existing code style in both stacks unless the user requests otherwise.

### General

- Prefer small, explicit modules and predictable naming.
- Keep changes scoped; avoid broad refactors unless requested.
- Preserve local-first assumptions (no cloud-only dependencies by default).
- Avoid adding new tooling config unless needed for the task.

### Python Backend Style

- Python version is not pinned in config; use modern syntax already present (`list[str]`, `X | None`).
- Keep `from __future__ import annotations` at the top of Python modules.
- Use type annotations on public functions and return types.
- Use `pydantic` models in `app/models/schemas.py` for request/response contracts.
- Keep route handlers thin; delegate behavior to `services/` modules.
- Use `snake_case` for functions, variables, module names.
- Use `PascalCase` for classes (e.g., `HealthService`, schema classes).
- Import order convention in current files:
  - standard library imports,
  - third-party imports,
  - local `app.*` imports.
- Prefer absolute imports from `app...` over deep relative imports.

Error handling:

- Catch narrow exception groups when parsing/IO can fail.
- Provide safe defaults on recoverable failures (see health metadata parsing).
- Raise HTTP errors explicitly in routes/services when implementing non-placeholder endpoints.

API conventions:

- Versioned routes under `/api/v1`.
- Keep response models explicit with `response_model=...`.
- For unimplemented endpoints, use `501` plus structured payloads.

### Frontend TypeScript/React Style

- TypeScript is strict (`"strict": true`).
- Additional compiler checks enabled: `noUnusedLocals`, `noUnusedParameters`.
- Use `import type` for type-only imports.
- Prefer explicit return types for exported functions.
- Use `camelCase` for vars/functions, `PascalCase` for React components/types.
- Keep API calls centralized in `src/api/`.
- Keep shared API types in `src/types/api.ts`.
- Use functional React components and hooks.
- Handle async UI states explicitly (`loading`, `sending`, fallback messages).

Formatting conventions observed:

- Double quotes in TS/TSX and Vite config.
- Semicolons are used consistently.
- 2-space indentation in frontend files.
- Keep JSX readable; avoid deeply nested inline logic.

Error handling:

- Wrap network calls with `try/catch`.
- Convert fetch failures to user-displayable messages.
- Preserve timeout/abort semantics in `requestJson`.

### CSS / UI

- Reuse existing CSS custom properties (`:root` variables).
- Keep layout responsive (existing breakpoint around `640px`).
- Prefer extending existing class structure over introducing parallel systems.

## Testing Guidance for Agents

- For backend logic changes: run at least focused pytest selection.
- For backend API changes: run the touched test file(s), then full backend test suite.
- For frontend changes: run `npm run build` to validate type-check + bundling.
- If you add frontend tests later, document exact single-test commands in this file.

## Change Management Guidance

- Do not silently change endpoint shapes without updating `docs/api/endpoints-v1.md`.
- Keep `.env` usage compatible with `pydantic-settings` (`RAG_` prefix).
- Keep CORS defaults aligned with local frontend hosts unless requirements change.
- Prefer incremental PR-sized changes over large rewrites.

## Quick Task Checklist for Agents

- Identify target area (`backend` vs `frontend`) first.
- Run minimal relevant verification commands before finishing.
- Update docs/contracts when behavior changes.
- Keep placeholder behavior (`ingest`/`query`) unless implementing them intentionally.
