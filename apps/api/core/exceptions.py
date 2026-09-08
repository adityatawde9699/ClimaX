"""
ClimaX Core Domain & API Exceptions
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class ClimaxBaseException(Exception):
    """Base exception for all ClimaX domain errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class EntityNotFoundException(ClimaxBaseException):
    """Raised when an entity is not found in database."""
    pass


class AIInferenceException(ClimaxBaseException):
    """Raised when Gemini or Vertex AI inference fails or produces unparseable output."""
    pass


class InvalidCoordinatesException(ClimaxBaseException):
    """Raised when coordinates fall outside valid WGS84 bounds."""
    pass


class UnauthorizedOperationException(ClimaxBaseException):
    """Raised when an operation violates RBAC permissions."""
    pass
