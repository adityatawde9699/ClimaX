"""Vercel FastAPI entrypoint for the API project built from the repo root.

The existing application uses ``apps/api`` as its import root for modules such
as ``core`` and ``api``. Keep that layout intact for local development while
making the same ASGI application discoverable by Vercel.
"""

import sys
from pathlib import Path

API_DIR = Path(__file__).resolve().parent / "apps" / "api"
sys.path.insert(0, str(API_DIR))

from main import app  # noqa: E402, F401
