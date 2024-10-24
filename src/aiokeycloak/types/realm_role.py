from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast
from uuid import UUID

from adaptix import NameStyle, Retort, name_mapping

from aiokeycloak.types.base import FromResponse, KeycloakType


@dataclass(frozen=True, slots=True)
class RoleRepresentationComposites(KeycloakType):
    realm: list[str] | None = None
    client: dict[Any, Any] | None = None


@dataclass(frozen=True, slots=True)
class RealmRole(KeycloakType):
    id: UUID | None = None
    name: str | None = None
    description: str | None = None
    scope_param_required: bool | None = None
    composite: bool | None = None
    composites: list[RoleRepresentationComposites] | None = None
    client_role: bool | None = None
    container_id: str | None = None
    attributes: dict[Any, Any] | None = None

    @classmethod
    def from_response(
        cls,
        data: FromResponse,
    ) -> RealmRole:
        return retort.load(data.body, cls)

    def serialize(self) -> dict[str, Any]:
        return cast(dict[str, Any], retort.dump(self))


retort = Retort(
    recipe=[
        name_mapping(
            RealmRole,
            name_style=NameStyle.CAMEL,
        ),
    ],
)
