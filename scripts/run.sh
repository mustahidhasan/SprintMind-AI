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

run_prisma_steps() {
  if command -v prisma >/dev/null 2>&1; then
    (cd backend && prisma generate || true)
    (cd backend && prisma migrate deploy || true)
  else
    echo "Prisma CLI not found, skipping prisma generate/migrate"
  fi
}

health_checks() {
  local endpoints=(
    "http://localhost:3000"
    "http://localhost:8000/api/v1/health"
    "http://localhost:8777/api/v1/health"
  )
  for url in "${endpoints[@]}"; do
    if curl -fsS "$url" >/dev/null; then
      echo "Health check passed: $url"
    else
      echo "Health check failed: $url"
      return 1
    fi
  done
}

run_dev() {
  require_paths
  ensure_env_file frontend/.env.dev frontend/.env.dev.example
  ensure_env_file backend/.env.dev backend/.env.dev.example
  ensure_env_file ai/.env.dev ai/.env.dev.example
  install_dependencies
  docker compose -f docker-compose.dev.yml up -d --build
  run_prisma_steps
  health_checks
}

run_prod() {
  require_paths
  [[ -f frontend/.env.prod && -f backend/.env.prod && -f ai/.env.prod ]] || {
    echo "Missing production env files"; exit 1;
  }
  docker compose -f docker-compose.prod.yml up -d --build
  run_prisma_steps
  health_checks
}

case "${1:-}" in
  --dev) run_dev ;;
  --prod) run_prod ;;
  *)
    echo "Usage: ./scripts/run.sh --dev|--prod"
    exit 1
    ;;
esac
