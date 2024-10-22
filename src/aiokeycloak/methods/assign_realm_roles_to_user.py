from dataclasses import dataclass
from uuid import UUID

from aiokeycloak.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeycloak.types.common import Success


@dataclass(frozen=True, slots=True)
class AssignRealmRolesToUser(KeycloakMethod[Success]):
    __url__ = "/admin/realms/{realm_name}/users/{user_id}/role-mappings/realm"
    __returning__ = Success
    __http_method__ = HTTPMethodType.POST

    access_token: str
    realm_name: str
    user_id: UUID
    realm_roles_names: list[str]

    def build_request_context(self) -> RequestContext:
        return RequestContext(
            body=[
                {"name": realm_role_name} for realm_role_name in self.realm_roles_names
            ],
            url_format={
                "realm_name": self.realm_name,
                "user_id": str(self.user_id),
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )
