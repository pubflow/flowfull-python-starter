# Architecture Overview

This starter aims to be productive, clear, and robust:

- FastAPI as the HTTP server
- Auth middleware based on Bridge Validation (Flowless)
- SQLAlchemy 2.x (async) for multi-dialect databases
- Hybrid cache: in-memory LRU + optional Redis
- Configuration via Pydantic Settings

## Components
- `app/main.py`: app creation, CORS, startup/shutdown events
- `app/routes/`: API and health routes with examples
- `app/lib/auth/`: session validation (Flowless), middleware, validation modes
- `app/lib/database/`: connection and async session helpers
- `app/models/`: SQLAlchemy models (e.g., `User`)

## Authentication Flow
1. Client sends `X-Session-Id` with requests.
2. Middleware validates against Flowless `/auth/bridge/validate` using `X-Bridge-Secret`.
3. If valid, `SessionData` is injected into your endpoint via `Depends()`.
4. Results are cached to accelerate subsequent requests.

## Supported Databases
- PostgreSQL and CockroachDB (asyncpg)
- MySQL (aiomysql)
- SQLite/LibSQL (aiosqlite)
Dialect detection is automatic based on `DATABASE_URL`.

## Request Lifecycle (High-Level)
- Incoming request → CORS → middleware parses headers → (optional) session validation → route handler → DB access via `AsyncSession` → response serialization

## Extending the Architecture
- Add new routes in `app/routes/` and protect them with `require_auth` or `require_user_type`.
- Define new models in `app/models/` and create migrations with Alembic.
- Introduce caching by using the hybrid cache instances in `app/lib/cache/`.