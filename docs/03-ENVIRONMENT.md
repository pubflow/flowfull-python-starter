# Environment Configuration

Create `.env` from `.env.example` and set the following:

- `DATABASE_URL`: `postgresql://`, `mysql://`, `sqlite://`, `libsql://`, `cockroachdb://`
- `FLOWLESS_API_URL`: URL of your Flowless instance (e.g., `https://api.pubflow.com`)
- `BRIDGE_VALIDATION_SECRET`: shared secret (min 32 chars)
- `AUTH_VALIDATION_MODE`: `DISABLED` | `STANDARD` | `ADVANCED` | `STRICT`
- `REDIS_URL` (optional): `redis://host:6379`
- CORS: `CORS_ORIGINS`, `CORS_METHODS`, `CORS_HEADERS`

Minimum example:
```
DATABASE_URL=postgresql://user:pass@localhost:5432/flowfull_db
FLOWLESS_API_URL=https://api.pubflow.com
BRIDGE_VALIDATION_SECRET=your-shared-secret
AUTH_VALIDATION_MODE=STANDARD
```

Dialect detection:
- `postgresql://...` → `postgresql+asyncpg://...` (strips `sslmode`)
- `cockroachdb://...` → `cockroachdb+asyncpg://...` (strips `sslmode`)
- `mysql://...` → `mysql+aiomysql://...`
- `sqlite://...` or `libsql://...` → `sqlite+aiosqlite://...`

Apply migrations:
```
alembic upgrade head
```

Windows notes:
- For local-only dev, prefer `--host 127.0.0.1`.
- For LAN access, add a Private inbound firewall rule for TCP 3001.