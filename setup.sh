#!/usr/bin/env bash
set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e "${BLUE}[info]${RESET}  $*"; }
success() { echo -e "${GREEN}[ok]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[warn]${RESET}  $*"; }
error()   { echo -e "${RED}[error]${RESET} $*" >&2; }

# ── Must run from project root ────────────────────────────────────────────────
if [ ! -f "docker-compose.yml" ]; then
  error "Run this script from the project root (where docker-compose.yml lives)."
  exit 1
fi

echo ""
echo -e "${BOLD}🎉  FestSync — setup${RESET}"
echo "────────────────────────────────────────"

# ── Check Docker ──────────────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
  error "Docker is not installed."
  echo "  → Install it from https://docs.docker.com/get-docker/"
  exit 1
fi
success "Docker found  ($(docker --version | cut -d' ' -f3 | tr -d ','))"

# ── Check Docker Compose ──────────────────────────────────────────────────────
if docker compose version &>/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose &>/dev/null; then
  COMPOSE="docker-compose"
else
  error "Docker Compose is not available."
  echo "  → Docker Desktop includes it, or install the plugin:"
  echo "    https://docs.docker.com/compose/install/"
  exit 1
fi
success "Docker Compose found  ($($COMPOSE version --short 2>/dev/null || echo 'v2'))"

# ── Create .env files from examples ──────────────────────────────────────────
if [ ! -f "frontend/.env" ]; then
  if [ -f "frontend/.env.example" ]; then
    cp frontend/.env.example frontend/.env
    warn "Created frontend/.env from .env.example — fill in your Supabase keys."
  else
    warn "frontend/.env.example not found, skipping."
  fi
else
  success "frontend/.env already exists"
fi

if [ ! -f "backend/.env" ]; then
  if [ -f "backend/.env.example" ]; then
    cp backend/.env.example backend/.env
    warn "Created backend/.env from .env.example — fill in your Supabase keys and DATABASE_URL."
  else
    warn "backend/.env.example not found, skipping."
  fi
else
  success "backend/.env already exists"
fi

# ── Start services ────────────────────────────────────────────────────────────
echo ""
info "Building and starting containers (this may take a few minutes on first run)…"
$COMPOSE up --build -d

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}✅  All services are running!${RESET}"
echo ""
echo -e "  ${BOLD}Frontend${RESET}   →  ${BLUE}http://localhost:3000${RESET}"
echo -e "  ${BOLD}Backend API${RESET} →  ${BLUE}http://localhost:8000${RESET}"
echo -e "  ${BOLD}API Docs${RESET}   →  ${BLUE}http://localhost:8000/docs${RESET}"
echo ""
echo -e "  ${YELLOW}Tip:${RESET} run ${BOLD}./stop.sh${RESET} to stop all containers."
echo ""
