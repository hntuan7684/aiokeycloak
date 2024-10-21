from dataclasses import dataclass
from typing import Any

from aiokeycloak.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeycloak.types.realm_roles import RealmRoles


@dataclass(frozen=True, slots=True)
class GetRealmRoles(KeycloakMethod[RealmRoles]):
    __url__ = "/admin/realms/{realm_name}/roles"
    __returning__ = RealmRoles
    __http_method__ = HTTPMethodType.GET

    realm_name: str
    access_token: str
    brief_representation: bool | None = None
    first: int | None = None
    max: int | None = None
    search: str | None = None

    def build_request_context(self) -> RequestContext:
        query_parameters: dict[str, Any] = {}
        if self.max:
            query_parameters["max"] = self.max
        if self.first:
            query_parameters["first"] = self.first
        if self.search:
            query_parameters["search"] = self.search
        if self.brief_representation:
            query_parameters["briefRepresentation"] = self.brief_representation

        return RequestContext(
            url_format={
                "realm_name": self.realm_name,
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            query_parameters=query_parameters or None,
        )
