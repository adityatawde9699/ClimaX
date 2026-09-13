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
if [ ! -f .env ]; then
  echo "Copying .env.example to .env..."
  cp .env.example .env
  echo "Created .env. Please configure your GCP & database settings."
else
  echo ".env already exists."
fi

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
echo "Setup complete! Start local services with: cd infrastructure/docker && docker compose up -d --build"
