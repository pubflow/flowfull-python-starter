# Core Concepts

Below are the seven core concepts with purpose, location, quick usage, and tips.

1. Bridge Validation
- Purpose: Validate sessions against Flowless and cache results.
- Location: `app/lib/auth/bridge_validator.py`
- Usage: Middleware calls `POST /auth/bridge/validate` with `X-Bridge-Secret`.
- Tips: Always include `X-Session-Id` header; rely on cache for performance.

2. Validation Modes
- Purpose: Control strictness of session validation.
- Location: `app/lib/auth/validation_mode.py`
- Modes: `DISABLED`, `STANDARD` (IP), `ADVANCED` (IP + UA), `STRICT` (IP + UA + Device)
- Tips: Use `STANDARD` for dev; increase strictness in production.

3. HybridCache
- Purpose: Multi-tier caching for session/profile/API data.
- Location: `app/lib/cache/*`
- Tiers: In-memory LRU; optional Redis for distributed environments.
- Tips: Configure `REDIS_URL` for horizontal scaling.

4. Trust Tokens (PASETO v4)
- Purpose: Issue secure tokens for trusted sub-systems.
- Location: `app/lib/tokens/trust_tokens.py`
- Usage: Generate keys via `scripts/generate_paseto_key.py`.
- Tips: Store keys securely; rotate regularly.

5. Auth Middleware
- Purpose: Protect routes and inject `SessionData`.
- Location: `app/lib/auth/middleware.py`
- Dependencies: `require_auth`, `optional_auth`, `require_user_type("admin", "superadmin")`
- Tips: Keep route auth minimal—business logic stays in handlers.

6. Multi-Database (Async ORM)
- Purpose: Connect to different databases automatically.
- Location: `app/lib/database/connection.py`
- Mapping: URL scheme → async dialect (postgresql+asyncpg, cockroachdb+asyncpg, mysql+aiomysql, sqlite+aiosqlite)
- Tips: `sslmode` is stripped where drivers don’t support it.

7. Environment Configuration
- Purpose: Centralized, type-safe settings.
- Location: `app/config/environment.py`
- Usage: `.env` file with validated variables.
- Tips: Fail-fast on invalid URLs; keep secrets out of source control.