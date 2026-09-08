# Contributing to ClimaX

Thank you for your interest in contributing to **ClimaX — Federated AI Environmental Intelligence & Action Platform**!

## Architecture & Code Principles

1. **Separation of Concerns**: Never mix domain logic into API route definitions or UI components.
2. **Strict Phase Adherence**: Follow the phased implementation plan outlined in the roadmap. Do not start Phase N+1 features before Phase N verification is completed.
3. **Typing & Contracts First**: All API interfaces, database models, and AI output payloads must adhere strictly to schemas defined in `packages/types/` and `apps/api/schemas/`.
4. **Trust & Explainability**: Every AI inference or prediction output must adhere to the 4-tier taxonomy (`OBSERVED`, `INFERRED`, `PREDICTED`, `VERIFIED`) with associated confidence and evidence metadata.
5. **No Hardcoded Secrets**: Use `.env` and `core/config.py`. Never commit tokens, credentials, or private keys.

---

## Development Workflow

### Prerequisites
- Node.js >= 20.0.0 & npm >= 10.0.0
- Python >= 3.11
- PostgreSQL 16+ with PostGIS extension enabled
- Docker (optional for local containerized development)

### Setting Up Local Environment

1. Clone repository and install dependencies:
   ```bash
   git clone <repo-url> climax
   cd climax
   cp .env.example .env
   ```

2. Setup Frontend dependencies:
   ```bash
   npm install
   ```

3. Setup Backend environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[ai,gcp,dev]"
   ```

### Code Formatting & Linting
- **Frontend**: `npm run lint:web`
- **Backend**: `npm run lint:api` or `ruff check .`
- **Verification**: `python3 scripts/verify-scaffolding.py`

---

## Commit & Pull Request Guidelines
- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- Reference applicable phase (e.g. `feat(phase-1): design system tokens`)
- All PRs must pass linting and architectural validation checks.
