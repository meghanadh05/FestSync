#!/usr/bin/env bash
set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

error() { echo -e "${RED}[error]${RESET} $*" >&2; }

# ── Must run from project root ────────────────────────────────────────────────
if [ ! -f "docker-compose.yml" ]; then
  error "Run this script from the project root (where docker-compose.yml lives)."
  exit 1
fi

# ── Pick compose command ──────────────────────────────────────────────────────
if docker compose version &>/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose &>/dev/null; then
  COMPOSE="docker-compose"
else
  error "Docker Compose is not available."
  exit 1
fi

echo ""
echo -e "${BOLD}🛑  FestSync — stopping containers…${RESET}"
$COMPOSE down
echo ""
echo -e "${GREEN}${BOLD}✅  All containers stopped.${RESET}"
echo -e "   Run ${BOLD}./setup.sh${RESET} to start again."
echo ""
