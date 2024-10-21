from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from adaptix import name_mapping, Retort

from aiokeycloak.types.base import KeycloakType


@dataclass(frozen=True, slots=True)
class RoleRepresentationComposites(KeycloakType):
    realm: list[str] | None = None
    client: dict[Any, Any] | None = None
    
    @classmethod
    def from_data(
        cls,
        data: Any,
    ) -> RoleRepresentationComposites:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class RealmRole(KeycloakType):
    attributes: dict[Any, Any] | None = None
    client_role: bool | None = None
    composite: bool | None = None
    composites: list[RoleRepresentationComposites] | None = None
    container_id: str | None = None
    description: str | None = None
    id: str | None = None
    name: str | None = None
    
    @classmethod
    def from_data(
        cls,
        data: dict[str, Any],
    ) -> RealmRole:
        return retort.load(data, cls)


retort = Retort(
    recipe=[
        name_mapping(
            RealmRole,
            map={
                'client_role': 'clientRole',
                'container_id': 'containerId',
            },
        ),
    ],
)
