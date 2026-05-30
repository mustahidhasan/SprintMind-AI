#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

require_paths() {
  local required=(frontend backend ai docker docker-compose.dev.yml docker-compose.prod.yml)
  for p in "${required[@]}"; do
    [[ -e "$p" ]] || { echo "Missing required path: $p"; exit 1; }
  done
}

ensure_env_file() {
  local target="$1"
  local example="$2"
  if [[ ! -f "$target" ]]; then
    cp "$example" "$target"
    echo "Created $target from $example"
  fi
}

install_dependencies() {
  (cd frontend && npm install)
  python3 -m venv backend/.venv
  backend/.venv/bin/pip install -r backend/requirements.txt
  python3 -m venv ai/.venv
  ai/.venv/bin/pip install -r ai/requirements.txt
}

run_migrations() {
  if docker ps --format '{{.Names}}' | rg -q '^sprintmind-ai-backend-1$'; then
    docker exec sprintmind-ai-backend-1 alembic -c alembic.ini upgrade head
  else
    echo "Backend container not running, skipping migrations"
  fi
}

health_checks() {
  local attempts=20
  local sleep_secs=2

  check_with_retry() {
    local url="$1"
    local i
    for ((i=1; i<=attempts; i++)); do
      if curl -fsS "$url" >/dev/null 2>&1; then
        echo "Health check passed: $url"
        return 0
      fi
      sleep "$sleep_secs"
    done
    return 1
  }

  check_in_container() {
    local container="$1"
    local url="$2"
    docker exec "$container" python -c "import httpx; r=httpx.get('$url', timeout=10); raise SystemExit(0 if r.status_code==200 else 1)" >/dev/null 2>&1
  }

  check_with_retry "http://localhost:3000" || { echo "Health check failed: http://localhost:3000"; return 1; }

  if check_with_retry "http://localhost:8000/api/v1/health"; then
    :
  elif check_in_container "sprintmind-ai-backend-1" "http://127.0.0.1:8000/api/v1/health"; then
    echo "Health check passed in-container: backend"
  else
    echo "Health check failed: backend"
    return 1
  fi

  if check_with_retry "http://localhost:8777/api/v1/health"; then
    :
  elif check_in_container "sprintmind-ai-ai-1" "http://127.0.0.1:8777/api/v1/health"; then
    echo "Health check passed in-container: ai"
  else
    echo "Health check failed: ai"
    return 1
  fi
}

print_urls() {
  cat <<TEXT
SprintMind AI is running

Frontend:   http://localhost:3000
Backend:    http://localhost:8000
AI Service: http://localhost:8777
Postgres:   localhost:5432
TEXT
}

run_dev() {
  require_paths
  ensure_env_file frontend/.env.dev frontend/.env.dev.example
  ensure_env_file backend/.env.dev backend/.env.dev.example
  ensure_env_file ai/.env.dev ai/.env.dev.example
  install_dependencies
  docker compose -f docker-compose.dev.yml up -d --build
  run_migrations
  health_checks
  print_urls
}

run_prod() {
  require_paths
  [[ -f frontend/.env.prod && -f backend/.env.prod && -f ai/.env.prod ]] || {
    echo "Missing production env files"; exit 1;
  }
  docker compose -f docker-compose.prod.yml up -d --build
  run_migrations
  health_checks
  print_urls
}

case "${1:-}" in
  --dev) run_dev ;;
  --prod) run_prod ;;
  *)
    echo "Usage: ./scripts/run.sh --dev|--prod"
    exit 1
    ;;
esac
