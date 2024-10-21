from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from aiokeyclock.types.realm_role import RealmRole
from aiokeyclock.types.base import KeycloakType


@dataclass(frozen=True, slots=True)
class RealmRoles(KeycloakType):
    roles: list[RealmRole]
    
    @classmethod
    def from_data(
        cls,
        data: Iterable[dict[str, Any]],
    ) -> RealmRoles:
        roles = []
        for datum in data:
            roles.append(RealmRole.from_data(datum))
        return cls(roles=roles)
