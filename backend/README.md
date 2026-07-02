# CloudFlow Backend

A FastAPI-based REST API for managing user profiles with MongoDB storage.

## Description

CloudFlow Backend provides a robust API for user profile management, built with FastAPI and MongoDB. It supports full CRUD operations for user profiles with automatic timestamps and CORS configuration for frontend integration.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database with Motor async driver
- **CRUD Operations** - Create, Read, Update, Delete user profiles
- **CORS Support** - Configurable cross-origin resource sharing
- **Docker Ready** - Containerized deployment support
- **Environment-based Config** - No hardcoded credentials

## Quick Start

1. **Install dependencies:**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export MONGO_URI="mongodb://admin:password@localhost:27017/cloudflow?authSource=admin"
   export DB_NAME="cloudflow"
   export FRONTEND_ORIGINS="http://localhost:3000"
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --port 3001
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/profiles` | Create a new profile |
| GET | `/api/profiles` | List all profiles |
| GET | `/api/profiles/{id}` | Get a specific profile |
| PATCH | `/api/profiles/{id}` | Update a profile |
| DELETE | `/api/profiles/{id}` | Delete a profile |

## Environment Variables

- `MONGO_URI` - MongoDB connection string (required)
- `DB_NAME` - Database name (required)
- `FRONTEND_ORIGINS` - Comma-separated allowed CORS origins (required)

## Docker

Build and run with Docker:

```bash
docker build -t cloudflow-backend .
docker run -p 3001:3001 --env-file .env cloudflow-backend
```

Or use Docker Compose (recommended for full stack).
