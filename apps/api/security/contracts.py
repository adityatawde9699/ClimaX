"""
ClimaX Security & Privacy Interfaces
Contract for token verification, RBAC authorization, and citizen PII/location obfuscation.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ISecurityService(ABC):
    @abstractmethod
    def create_access_token(self, user_id: str, role: str, expires_delta: Optional[int] = None) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def obfuscate_citizen_coordinates(self, lat: float, lng: float, blur_radius_m: float = 200.0) -> tuple[float, float]:
        """Obfuscates exact citizen report coordinates for public display while retaining analytical utility."""
        pass
