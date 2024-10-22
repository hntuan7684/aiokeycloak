from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class FromResponse:
    body: Any
    headers: dict[str, Any]


class KeycloakType(Protocol):
    @classmethod
    def from_response(
        cls,
        data: FromResponse,
    ) -> KeycloakType:
        raise NotImplementedError

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError
