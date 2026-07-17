# Flowfull Python Starter

Production-ready Python backend template with Flowless integration, built with FastAPI and modern async patterns.

## 🚀 Features

### 7 Core Concepts

1. **Bridge Validation** - Distributed session validation with Flowless
2. **Validation Modes** - Layered security (DISABLED, STANDARD, ADVANCED, STRICT)
3. **HybridCache** - 3-tier caching system (LRU + Redis + Database)
4. **Trust Tokens** - Secure PASETO v4 token management
5. **Auth Middleware** - FastAPI dependencies for route protection
6. **Multi-Database** - Support for PostgreSQL, MySQL, and SQLite
7. **Environment Config** - Type-safe configuration with Pydantic

### Technology Stack

- **Python 3.11+** - Modern Python with type hints
- **FastAPI 0.115+** - High-performance async web framework
- **SQLAlchemy 2.x** - Async ORM with multi-database support
- **Pydantic 2.x** - Data validation and settings management
- **Redis** - Distributed caching layer
- **PASETO v4** - Secure token generation
- **Structlog** - Structured logging
- **Pytest** - Comprehensive testing framework

## 📦 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd flowfull-python-starter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

**Minimum required configuration:**

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/flowfull_db
FLOWLESS_API_URL=https://your-instance.pubflow.com
BRIDGE_VALIDATION_SECRET=your-shared-secret-min-32-chars
```

### 3. Database Setup

```bash
# Run migrations
alembic upgrade head
```

### 4. Run Development Server

```bash
# Start server with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 3001

# Server will be available at:
# - API: http://localhost:3001
# - Docs: http://localhost:3001/docs
# - Health: http://localhost:3001/health
```
        
## 🐳 Docker

### Using Docker Compose

```bash
# Start all services (app + PostgreSQL + Redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Build Docker Image

```bash
# Build image
docker build -t flowfull-python .

# Run container
docker run -p 3001:3001 --env-file .env flowfull-python
```

## 📚 Documentation

Friendly documentation is available in the `/docs` directory:

- **[00-ARCHITECTURE-OVERVIEW.md](./docs/00-ARCHITECTURE-OVERVIEW.md)** - System architecture and diagrams
- **[02-CORE-CONCEPTS.md](./docs/02-CORE-CONCEPTS.md)** - Implementation of 7 core concepts
- **[03-ENVIRONMENT.md](./docs/03-ENVIRONMENT.md)** - Environment configuration guide
- **[04-USAGE-GUIDE.md](./docs/04-USAGE-GUIDE.md)** - Complete usage examples
- **[QUICK-REFERENCE.md](./docs/QUICK-REFERENCE.md)** - Quick reference guide

## 🔧 Development

### Code Quality

```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
ruff check app/ tests/

# Type checking
mypy app/

# Run all checks
black app/ tests/ && isort app/ tests/ && ruff check app/ tests/ && mypy app/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_health.py

# Run with verbose output
pytest -v
```

## 📖 Usage Examples

### Public Route (No Authentication)

```python
@router.get("/public")
async def public_route() -> dict:
    return {"message": "This is public"}
```

### Protected Route (Authentication Required)

```python
from app.lib.auth.middleware import require_auth
from app.lib.auth.bridge_validator import SessionData

@router.get("/profile")
async def get_profile(session: SessionData = Depends(require_auth)) -> dict:
    return {
        "user_id": session.user_id,
        "email": session.email,
        "name": session.name
    }
```

### Optional Authentication

```python
from app.lib.auth.middleware import optional_auth

@router.get("/content")
async def get_content(session: Optional[SessionData] = Depends(optional_auth)) -> dict:
    if session:
        return {"message": f"Hello {session.name}!"}
    return {"message": "Hello guest!"}
```

### User Type Restriction

```python
from app.lib.auth.middleware import require_admin, require_user_type

@router.get("/admin")
async def admin_route(session: SessionData = Depends(require_admin)) -> dict:
    return {"message": "Admin access granted"}
```

### Using HybridCache

```python
from app.lib.cache.cache_instances import profile_cache

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    # Check cache first
    user = await profile_cache.get(user_id)
    if user:
        return {"user": user, "cached": True}

    # Fetch from database
    user = await fetch_user_from_db(user_id)

    # Cache for future requests
    await profile_cache.set(user_id, user, ttl=600)

    return {"user": user, "cached": False}
```

## 🔐 Security

### Validation Modes

Configure session validation strictness in `.env`:

```env
# DISABLED - No validation (development only)
# STANDARD - IP validation
# ADVANCED - IP + User-Agent validation
# STRICT - IP + User-Agent + Device ID validation
AUTH_VALIDATION_MODE=STANDARD
```

### Trust Tokens (PASETO)

Generate a secure PASETO key:

```bash
python scripts/generate_paseto_key.py
```

Add the generated key to your `.env` file:

```env
PASETO_PRIVATE_KEY=k4.local.your-generated-key-here
```

## 🏗️ Project Structure

```
flowfull-python-starter/
├── app/
│   ├── config/
│   │   └── environment.py         # Pydantic settings
│   ├── lib/
│   │   ├── auth/
│   │   │   ├── bridge_validator.py    # Session validation
│   │   │   ├── middleware.py          # Auth dependencies
│   │   │   └── validation_mode.py     # Validation modes
│   │   ├── cache/
│   │   │   ├── hybrid_cache.py        # 3-tier cache
│   │   │   └── cache_instances.py     # Cache instances
│   │   ├── database/
│   │   │   ├── connection.py          # Database setup
│   │   │   └── session.py             # Session helpers
│   │   ├── tokens/
│   │   │   └── trust_tokens.py        # PASETO tokens
│   │   └── utils/
│   │       └── logger.py              # Structured logging
│   ├── models/
│   │   └── user.py                # Example model
│   ├── routes/
│   │   ├── health.py              # Health checks
│   │   └── api.py                 # API routes
│   └── main.py                    # FastAPI app
├── tests/
│   ├── conftest.py                # Pytest fixtures
│   ├── test_health.py             # Health tests
│   └── test_api.py                # API tests
├── scripts/
│   └── generate_paseto_key.py     # Key generation
├── alembic/                       # Database migrations
├── .env.example                   # Environment template
├── pyproject.toml                 # Project config
├── requirements.txt               # Dependencies
├── Dockerfile                     # Docker config
└── docker-compose.yml             # Docker Compose
```

## 🚀 Deployment

### Environment Variables

Required for production:

```env
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:5432/db
FLOWLESS_API_URL=https://your-instance.pubflow.com
BRIDGE_VALIDATION_SECRET=your-production-secret-min-32-chars
PASETO_PRIVATE_KEY=k4.local.your-production-key
REDIS_URL=redis://redis-host:6379
CORS_ORIGINS=https://yourdomain.com
```

### Production Server

```bash
# Using Uvicorn with workers
uvicorn app.main:app --host 0.0.0.0 --port 3001 --workers 4

# Using Gunicorn with Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3001
```

## 📊 Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Cache Hit Rate | >90% | LRU + Redis |
| Auth Latency (cached) | <5ms | LRU hit |
| Auth Latency (Redis) | <15ms | Redis hit |
| Auth Latency (Bridge) | <100ms | Flowless validation |
| Request Throughput | >10k req/s | With cache |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- **Flowless Documentation**: [Flowless Docs](https://docs.pubflow.com)
- **FastAPI Documentation**: [FastAPI](https://fastapi.tiangolo.com)
- **Pydantic Documentation**: [Pydantic](https://docs.pydantic.dev)
- **SQLAlchemy Documentation**: [SQLAlchemy](https://docs.sqlalchemy.org)

## 💬 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `/to-do` directory
- Contact: support@pubflow.com

---

**Built with ❤️ by the Pubflow Team**


