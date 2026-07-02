# CloudFlow Backend

A FastAPI-based REST API for managing user profiles, backed by PostgreSQL via SQLAlchemy 2.x async (asyncpg). Part of the `devops-assessment` monorepo — see the root [README.md](../README.md) for full-stack setup with Docker Compose.

## Description

CloudFlow Backend provides a robust API for user profile management, built with FastAPI and PostgreSQL. It supports full CRUD operations for user profiles with automatic timestamps and CORS configuration for frontend integration.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Relational database via SQLAlchemy 2.x async engine (asyncpg driver)
- **CRUD Operations** - Create, Read, Update, Delete user profiles
- **CORS Support** - Configurable cross-origin resource sharing
- **Docker Ready** - Multi-stage, non-root production image
- **Environment-based Config** - No hardcoded credentials; fails fast if required vars are missing
- **Liveness endpoints** - `GET /` and `GET /health` (the latter never touches the database)

## Quick Start

1. **Install dependencies:**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export DATABASE_URL="postgresql+asyncpg://appuser:change-me@localhost:5432/appdb"
   export FRONTEND_ORIGINS="http://localhost:3000"
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   ```

   In the Docker Compose stack (see root README) the app always runs on port `8080`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Liveness check — returns `"Application is running"` |
| GET | `/health` | Liveness check — returns `{"status": "ok"}`; never touches the database |
| POST | `/api/profiles` | Create a new profile |
| GET | `/api/profiles` | List all profiles |
| GET | `/api/profiles/{id}` | Get a specific profile |
| PATCH | `/api/profiles/{id}` | Update a profile |
| DELETE | `/api/profiles/{id}` | Delete a profile |

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string, e.g. `postgresql+asyncpg://user:pass@db:5432/appdb` (required)
- `FRONTEND_ORIGINS` - Comma-separated allowed CORS origins (required)

Both are validated at import time; the app raises a single `RuntimeError` listing every missing variable if either is unset. There are no hardcoded fallback credentials.

## Tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

Tests run against an in-memory SQLite database via a `dependency_overrides` swap — no PostgreSQL instance is required.

## Docker

Build and run with Docker:

```bash
docker build -t cloudflow-backend .
docker run -p 8080:8080 --env-file .env cloudflow-backend
```

Or use Docker Compose from the repo root (recommended for the full stack) — see the root [README.md](../README.md).
