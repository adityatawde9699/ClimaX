"""
Global Pytest Fixtures Configuration for ClimaX
"""

import sys
from pathlib import Path
import pytest

# Ensure apps/api is importable in test suites
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir / "apps" / "api"))
