# Getting Started with Flowfull Python Starter

This guide will help you get up and running with the Flowfull Python Starter in minutes.

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL, MySQL, or SQLite (for development)
- Redis (optional, for distributed caching)
- Flowless instance URL and Bridge Validation Secret

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone and Install

```bash
# Navigate to the project directory
cd flowfull-python-starter

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Required - Database
DATABASE_URL=postgresql://user:password@localhost:5432/flowfull_db

# Required - Flowless Integration
FLOWLESS_API_URL=https://your-instance.pubflow.com
BRIDGE_VALIDATION_SECRET=your-shared-secret-min-32-chars

# Optional - Redis (recommended for production)
REDIS_URL=redis://localhost:6379

# Optional - CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 3: Generate PASETO Key (Optional)

If you plan to use trust tokens:

```bash
python scripts/generate_paseto_key.py
```

Copy the generated key to your `.env` file:

```env
PASETO_PRIVATE_KEY=k4.local.your-generated-key-here
```

### Step 4: Setup Database

```bash
# Run migrations
alembic upgrade head
```

### Step 5: Start Development Server

```bash
# Start with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 3001
```

Your server is now running! 🎉

- **API**: http://localhost:3001
- **Docs**: http://localhost:3001/docs
- **Health**: http://localhost:3001/health

## 🧪 Verify Installation

### 1. Check Health Endpoint

```bash
curl http://localhost:3001/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000",
  "environment": "development",
  "version": "0.1.0"
}
```

### 2. Check Public Route

```bash
curl http://localhost:3001/api/v1/public
```

Expected response:
```json
{
  "message": "This is a public route",
  "timestamp": "2024-01-01T00:00:00.000000",
  "authenticated": false
}
```

### 3. Run Tests

```bash
pytest
```

All tests should pass! ✅

## 🐳 Using Docker (Alternative)

If you prefer Docker:

```bash
# Start all services (app + PostgreSQL + Redis)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

## 📖 Next Steps

### 1. Understand the 7 Core Concepts

Read the documentation in `/to-do` directory:

- **Bridge Validation**: Session validation with Flowless
- **Validation Modes**: Security levels (DISABLED, STANDARD, ADVANCED, STRICT)
- **HybridCache**: 3-tier caching system
- **Trust Tokens**: PASETO v4 token management
- **Auth Middleware**: Route protection
- **Multi-Database**: Database flexibility
- **Environment Config**: Type-safe configuration

### 2. Explore Example Routes

Open http://localhost:3001/docs to see:

- **Public routes**: No authentication required
- **Protected routes**: Authentication required
- **Optional auth routes**: Enhanced experience for authenticated users
- **User type restricted routes**: Role-based access control

### 3. Create Your First Protected Route

Edit `app/routes/api.py`:

```python
from app.lib.auth.middleware import require_auth
from app.lib.auth.bridge_validator import SessionData

@router.get("/my-route")
async def my_route(session: SessionData = Depends(require_auth)) -> dict:
    return {
        "message": f"Hello {session.name}!",
        "user_id": session.user_id
    }
```

### 4. Add Your First Model

Create a new model in `app/models/`:

```python
from sqlalchemy import Column, String, DateTime
from app.lib.database.connection import Base

class MyModel(Base):
    __tablename__ = "my_table"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

Generate migration:

```bash
alembic revision --autogenerate -m "Add my_table"
alembic upgrade head
```

## 🔧 Common Issues

### Issue: Database Connection Error

**Solution**: Verify your `DATABASE_URL` in `.env` is correct and the database server is running.

```bash
# Test PostgreSQL connection
psql -h localhost -U your_user -d your_database

# Test MySQL connection
mysql -h localhost -u your_user -p your_database
```

### Issue: Redis Connection Error

**Solution**: Redis is optional. If not using Redis, the system will fall back to LRU cache only.

```bash
# Test Redis connection
redis-cli ping
# Should return: PONG
```

### Issue: Import Errors

**Solution**: Make sure you're in the virtual environment and dependencies are installed.

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## 📚 Documentation

- **[README.md](./README.md)** - Project overview
- **[to-do/QUICK-REFERENCE.md](./to-do/QUICK-REFERENCE.md)** - Quick reference guide
- **[to-do/04-USAGE-GUIDE.md](./to-do/04-USAGE-GUIDE.md)** - Detailed usage examples
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Implementation details

## 💬 Need Help?

- Check the `/to-do` directory for comprehensive documentation
- Open an issue on GitHub
- Contact: support@pubflow.com

---

**You're all set! Start building your application! 🚀**

