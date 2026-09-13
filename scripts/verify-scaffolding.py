#!/usr/bin/env python3
"""
ClimaX Scaffolding & Architecture Verification Script
Performs automated static validation of repository structure, files, schemas, and Phase 0 hygiene.
"""

import json
import sys
from pathlib import Path

REQUIRED_DIRECTORIES = [
    "apps/web",
    "apps/web/app",
    "apps/web/components",
    "apps/web/features",
    "apps/web/features/citizen",
    "apps/api",
    "apps/api/api/v1",
    "apps/api/core",
    "apps/api/models",
    "apps/api/schemas",
    "apps/api/repositories",
    "apps/api/services",
    "apps/api/integrations",
    "apps/api/ai",
    "apps/api/prediction",
    "apps/api/geospatial",
    "apps/api/events",
    "apps/api/workers",
    "apps/api/security",
    "apps/api/observability",
    "packages/types",
    "packages/ui",
    "packages/config",
    "packages/utils",
    "services/ai",
    "services/prediction",
    "services/geospatial",
    "services/environmental-data",
    "services/alerts",
    "services/analytics",
    "data/schemas",
    "data/samples",
    "data/fixtures",
    "infrastructure/docker",
    "infrastructure/gcp",
    "infrastructure/database",
    "infrastructure/deployment",
    "docs/architecture",
    "docs/product",
    "docs/ai",
    "docs/data",
    "docs/decisions",
    "tests/architecture",
]

REQUIRED_FILES = [
    "README.md",
    ".env.example",
    ".gitignore",
    "package.json",
    "pyproject.toml",
    "ruff.toml",
    "CONTRIBUTING.md",
    "LICENSE",
    "apps/web/package.json",
    "apps/web/tsconfig.json",
    "apps/web/tailwind.config.ts",
    "apps/web/app/layout.tsx",
    "apps/web/app/page.tsx",
    "apps/api/main.py",
    "apps/api/core/config.py",
    "apps/api/models/entities.py",
    "apps/api/schemas/entities.py",
    "apps/api/schemas/ai.py",
    "apps/api/api/v1/router.py",
    "packages/types/package.json",
    "packages/types/src/entities.ts",
    "packages/types/src/ai.ts",
    "packages/ui/src/tokens.ts",
    "packages/utils/src/geo.ts",
    "data/schemas/ai_analysis.schema.json",
    "data/samples/ai_analysis_sample.json",
    "data/samples/observation_sample.json",
    "infrastructure/docker/docker-compose.yml",
    "infrastructure/database/0001_initial_schema.sql",
    "docs/architecture/system-architecture.md",
    "docs/architecture/frontend-architecture.md",
    "docs/architecture/backend-architecture.md",
    "docs/architecture/ai-architecture.md",
    "docs/architecture/data-architecture.md",
    "docs/architecture/geospatial-architecture.md",
    "docs/architecture/security.md",
    "docs/architecture/observability.md",
    "docs/product/product-overview.md",
    "docs/product/user-roles.md",
    "docs/ai/trust-and-explainability.md",
    "docs/data/data-sources.md",
    "docs/decisions/README.md",
]


def main():
    root = Path(__file__).resolve().parent.parent
    print(f"Verifying ClimaX repository scaffolding at: {root}")
    errors = []

    # 1. Check directories
    for d in REQUIRED_DIRECTORIES:
        path = root / d
        if not path.is_dir():
            errors.append(f"Missing required directory: {d}")

    # 2. Check files
    for f in REQUIRED_FILES:
        path = root / f
        if not path.is_file():
            errors.append(f"Missing required file: {f}")

    # 3. Validate JSON files
    json_files = list(root.glob("**/*.json"))
    for jf in json_files:
        if "node_modules" in str(jf) or ".next" in str(jf):
            continue
        try:
            with open(jf) as file:
                json.load(file)
        except Exception as e:
            errors.append(f"Invalid JSON in {jf.relative_to(root)}: {e}")

    # 4. Check for prohibited secret patterns in repository
    sensitive_tokens = ["AIza" + "Sy", "xox" + "b-", "gh" + "p_"]
    for path in root.rglob("*"):
        if path.is_file() and not any(
            ignored in str(path)
            for ignored in [".git", "node_modules", ".venv", "__pycache__", "scripts", "tests"]
        ):
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                for token in sensitive_tokens:
                    if token in content:
                        errors.append(
                            f"Potential secret pattern detected in {path.relative_to(root)}"
                        )
            except Exception:
                pass

    if errors:
        print("\n❌ Verification FAILED with errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(
            "\n✅ Verification PASSED: All 40+ architectural directories, 35+ core files, schemas, and hygiene rules verified!"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
