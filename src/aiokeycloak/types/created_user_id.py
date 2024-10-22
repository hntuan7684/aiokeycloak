from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from aiokeycloak.types.base import FromResponse, KeycloakType


@dataclass(frozen=True, slots=True)
class CreatedUserId(KeycloakType):
    user_id: UUID

    @classmethod
    def from_response(
        cls,
        data: FromResponse,
    ) -> CreatedUserId:
        location = data.headers["Location"]
        return cls(UUID(location.split("/")[-1]))
