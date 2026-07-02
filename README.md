# DevOps Assessment

User profile manager: Next.js frontend, FastAPI backend, PostgreSQL database, all containerized.

## Architecture

    browser --> frontend:3000 --[Next.js rewrite /api/*]--> backend:8080 --> postgres:5432

The browser only ever talks to the frontend container. The frontend forwards
`/api/*` requests server-side to the backend using a Next.js rewrite rule.

## Prerequisites

- Docker and Docker Compose

## Run

    cp .env.example .env
    docker compose up -d --build

## Verify

    curl http://localhost:8080          # "Application is running"
    curl http://localhost:8080/health   # {"status":"ok"}

Open http://localhost:3000 and create/edit/delete a profile. Data persists
across `docker compose restart backend` because Postgres uses a named volume.

## Backend tests

    cd backend
    python3.12 -m venv .venv && source .venv/bin/activate
    pip install -r requirements-dev.txt
    pytest -v

No database needs to be running — tests use an in-memory SQLite override.

## Environment variables

| Service  | Variable          | Example                                              | Notes                              |
|----------|-------------------|-------------------------------------------------------|-------------------------------------|
| db       | POSTGRES_USER     | appuser                                                | from `.env`                         |
| db       | POSTGRES_PASSWORD | change-me                                              | from `.env`                         |
| db       | POSTGRES_DB       | appdb                                                  | from `.env`                         |
| backend  | DATABASE_URL      | postgresql+asyncpg://appuser:change-me@db:5432/appdb   | composed by compose from `.env`     |
| backend  | FRONTEND_ORIGINS  | http://localhost:3000                                  | comma-separated CORS origins        |
| frontend | BACKEND_URL       | http://backend:8080                                    | server-side only, used by rewrites  |

## Design decisions

The frontend never calls the backend directly from the browser. Instead it
proxies through a Next.js rewrite so `BACKEND_URL` stays a server-side
runtime variable, never baked into the client bundle. This keeps the
backend's network location swappable without a frontend rebuild, and lets
the backend run as an internal-only (ClusterIP) service once this stack
moves to Kubernetes in a later phase. The backend's `8080` host-port
mapping in `docker-compose` is only a local-verification convenience for
this phase and would drop away entirely (no host port, ClusterIP-only)
once the Kubernetes phase lands.
