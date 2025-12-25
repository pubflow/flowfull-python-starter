# Quick Reference

## Commands
```
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Migrations
alembic upgrade head

# Development (local-only)
uvicorn app.main:app --host 127.0.0.1 --port 3001

# Development (LAN / Windows)
New-NetFirewallRule -DisplayName "Flowfull Dev 3001" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 3001 -Profile Private
uvicorn app.main:app --host 0.0.0.0 --port 3001
```

## Auth
- Header: `X-Session-Id`
- Bridge header: `X-Bridge-Secret` (server-side)
- `SessionData` is injected via dependencies.

## Middleware
- `require_auth`
- `optional_auth`
- `require_user_type("admin", "superadmin")`

## Database
- `DATABASE_URL` auto-detects dialect.
- Drivers: asyncpg, aiomysql, aiosqlite.

## Useful routes
- `/api/v1/health`
- `/api/v1/profile`
- `/api/v1/admin/users`