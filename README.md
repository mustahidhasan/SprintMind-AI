# SprintMind-AI

Runbook for local development and production-style Docker runs.

## Prerequisites

- Docker Desktop running
- `bash`
- `curl`
- `python3`
- `node` + `npm`

## Project Structure

- `frontend` -> Next.js app (port `3000`)
- `backend` -> FastAPI app (port `8000`)
- `ai` -> AI service (port `8777`, used in prod compose)
- `postgres` -> PostgreSQL (port `5432`, dev compose)

## 1) Development (First)

### Quick start (recommended)

```bash
bash scripts/run.sh --dev
```

What this does:

- Creates missing env files from examples
- Installs frontend/backend dependencies
- Builds and starts dev Docker services
- Runs backend migrations
- Runs basic health checks

### Dev env files

If needed, create manually:

```bash
cp frontend/.env.dev.example frontend/.env.dev
cp backend/.env.dev.example backend/.env.dev
```

### Start/stop dev stack manually

```bash
# start (build + detached)
docker compose -f docker-compose.dev.yml up -d --build

# view logs
docker logs sprintmind-ai-frontend-1 --tail 200
docker logs sprintmind-ai-backend-1 --tail 200
docker logs sprintmind-ai-postgres-1 --tail 200

# stop
docker compose -f docker-compose.dev.yml down
```

### Dev health checks

```bash
curl -sS -i http://localhost:3000
curl -sS -i http://localhost:8000/api/v1/health
```

Expected backend response includes:

```json
{"success":true,"status":"ok","service":"backend"}
```

### Dev notes

- Backend migrations are executed on container startup.
- If UI changes do not appear, rebuild frontend container:

```bash
docker compose -f docker-compose.dev.yml up -d --build frontend
```

## 2) Production (Second)

### Required env files

Create and configure these before running prod:

```bash
cp frontend/.env.prod.example frontend/.env.prod
cp backend/.env.prod.example backend/.env.prod
cp ai/.env.prod.example ai/.env.prod
```

### Required shell env vars (used by deploy script)

```bash
export DATABASE_URL="<your_database_url>"
export JWT_SECRET="<your_jwt_secret>"
export ENCRYPTION_KEY="<your_encryption_key>"
```

### Run prod stack using run script

```bash
bash scripts/run.sh --prod
```

### Deploy-oriented script (build + checks)

```bash
bash scripts/deploy.sh --prod
```

This script:

- Validates required env files/vars
- Builds Docker images
- Attempts tests/migrations when tools exist
- Starts prod compose stack
- Runs health checks

### Prod compose direct commands

```bash
# start
docker compose -f docker-compose.prod.yml up -d --build

# logs
docker logs sprintmind-ai-frontend-1 --tail 200
docker logs sprintmind-ai-backend-1 --tail 200
docker logs sprintmind-ai-ai-1 --tail 200

# stop
docker compose -f docker-compose.prod.yml down
```

### Prod health checks

```bash
curl -sS -i http://localhost:3000
curl -sS -i http://localhost:8000/api/v1/health
curl -sS -i http://localhost:8777/api/v1/health
```

## Troubleshooting

### APIs failing / CRUD not working

1. Ensure containers are up:

```bash
docker ps
```

2. Check backend + DB logs:

```bash
docker logs sprintmind-ai-backend-1 --tail 300
docker logs sprintmind-ai-postgres-1 --tail 300
```

3. Rebuild and restart cleanly:

```bash
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml up -d --build
```

4. Verify backend health again:

```bash
curl -sS -i http://localhost:8000/api/v1/health
```

## Script Reference

- Dev/prod run: `bash scripts/run.sh --dev|--prod`
- Dev/prod deploy: `bash scripts/deploy.sh --dev|--prod`

