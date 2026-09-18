import pytest
from pydantic import ValidationError

from core.config import Settings


def test_production_rejects_development_defaults():
    with pytest.raises(ValidationError, match="Invalid production configuration"):
        Settings(ENVIRONMENT="production", _env_file=None)
