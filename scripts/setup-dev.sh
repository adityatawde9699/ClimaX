#!/usr/bin/env bash
# ==============================================================================
# ClimaX Local Development Bootstrap Script
# ==============================================================================
set -euo pipefail

echo "================================================="
echo "  ClimaX Platform — Developer Environment Setup  "
echo "================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

# 1. Environment template check
for app in api web; do
  if [ ! -f "apps/${app}/.env" ]; then
    cp "apps/${app}/.env.example" "apps/${app}/.env"
    echo "Created apps/${app}/.env. Configure it for your environment."
  else
    echo "apps/${app}/.env already exists."
  fi
done

# 2. Python Virtual Environment
if [ ! -d .venv ]; then
  echo "Setting up Python virtual environment (.venv)..."
  python3 -m venv .venv
fi
echo "Activating virtual environment..."
source .venv/bin/activate

# 3. Install local dependencies
echo "Installing Python development dependencies..."
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

echo "Installing workspace dependencies..."
npm install

# 4. Verify scaffolding
echo "Running scaffolding verification..."
python3 scripts/verify-scaffolding.py

echo ""
echo "Setup complete! Start local services with: docker compose --env-file apps/web/.env -f infrastructure/docker/docker-compose.yml up -d --build"
