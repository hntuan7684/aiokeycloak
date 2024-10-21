from __future__ import annotations

from abc import abstractmethod
from typing import Any, Protocol


class KeycloakType(Protocol):
    @classmethod
    @abstractmethod
    def from_data(
        cls,
        data: Any,
    ) -> KeycloakType:
        raise NotImplementedError
