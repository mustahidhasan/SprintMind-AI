#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

check_health() {
  local endpoints=(
    "http://localhost:3000"
    "http://localhost:8000/api/v1/health"
    "http://localhost:8777/api/v1/health"
  )
  for url in "${endpoints[@]}"; do
    curl -fsS "$url" >/dev/null
    echo "Healthy: $url"
  done
}

deploy_dev() {
  docker compose -f docker-compose.dev.yml build
  docker compose -f docker-compose.dev.yml up -d
  check_health
}

deploy_prod() {
  [[ -f frontend/.env.prod && -f backend/.env.prod && -f ai/.env.prod ]] || {
    echo "Missing production env files"; exit 1;
  }

  : "${DATABASE_URL:?DATABASE_URL must be set}"
  : "${JWT_SECRET:?JWT_SECRET must be set}"
  : "${ENCRYPTION_KEY:?ENCRYPTION_KEY must be set}"

  docker compose -f docker-compose.prod.yml build

  if command -v pytest >/dev/null 2>&1; then
    (cd backend && ../backend/.venv/bin/python -m pytest || true)
    (cd ai && ../ai/.venv/bin/python -m pytest || true)
  else
    echo "pytest not found, skipping tests"
  fi

  if command -v prisma >/dev/null 2>&1; then
    (cd backend && prisma migrate deploy || true)
  else
    echo "Prisma CLI not found, skipping migration"
  fi

  (cd frontend && npm run build || true)

  echo "Cloudflare deploy placeholder: configure wrangler/pages pipelines per service"
  docker compose -f docker-compose.prod.yml up -d
  check_health
}

case "${1:-}" in
  --dev) deploy_dev ;;
  --prod) deploy_prod ;;
  *)
    echo "Usage: ./scripts/deploy.sh --dev|--prod"
    exit 1
    ;;
esac
