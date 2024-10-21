from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiokeycloak.types.base import KeycloakType


class Success(KeycloakType):
    @classmethod
    def from_data(
        cls,
        data: Any,
    ) -> Success:
        return cls()


@dataclass(frozen=True, slots=True)
class Raw(KeycloakType):
    data: Any
    
    @classmethod
    def from_data(
        cls,
        data: Any,
    ) -> Raw:
        return cls(data)
