# Usage Guide

## Start the server
```
uvicorn app.main:app --host 127.0.0.1 --port 3001
```
Windows (LAN access):
```
New-NetFirewallRule -DisplayName "Flowfull Dev 3001" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 3001 -Profile Private
uvicorn app.main:app --host 0.0.0.0 --port 3001
```

## Example routes
- Public: `/api/v1/public`
- Profile (auth): `/api/v1/profile`
- Admin-only: `/api/v1/admin/users`, `/api/v1/users`, `/api/v1/users/{user_id}`

## Add routes
```
from fastapi import Depends
from app.lib.auth.bridge_validator import SessionData
from app.lib.auth.middleware import require_auth, require_user_type

@router.get("/hello")
async def hello(session: SessionData = Depends(require_auth)):
    return {"message": f"Hello {session.name}"}

@router.get("/admin/reports")
async def reports(session: SessionData = Depends(require_user_type("admin"))):
    return {"reports": []}
```

## Models and DB
- Define models in `app/models/*`.
- Use `select(Model)` with `AsyncSession` from `get_db`.
- Create/update tables with Alembic.

## Tips
- Use `optional_auth` for mixed content routes.
- Cache frequent reads with HybridCache.