from __future__ import annotations

from dataclasses import dataclass

from aiokeycloak.types.realm_role import RealmRole
from aiokeycloak.types.base import FromResponse, KeycloakType


@dataclass(frozen=True, slots=True)
class RealmRoles(KeycloakType):
    roles: list[RealmRole]

    @classmethod
    def from_response(
        cls,
        data: FromResponse,
    ) -> RealmRoles:
        roles = []
        for body in data.body:
            roles.append(
                RealmRole.from_response(
                    FromResponse(
                        body=body,
                        headers=data.headers,
                    ),
                ),
            )
        return cls(roles=roles)
