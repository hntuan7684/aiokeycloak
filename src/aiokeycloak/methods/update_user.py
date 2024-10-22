from dataclasses import dataclass
from uuid import UUID

from aiokeycloak.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeycloak.types.common import Success
from aiokeycloak.types.user import User


@dataclass(frozen=True, slots=True)
class UpdateUser(KeycloakMethod[Success]):
    __url__ = "/admin/realms/{realm_name}/users/{user_id}"
    __returning__ = Success
    __http_method__ = HTTPMethodType.PUT

    access_token: str
    realm_name: str
    user_id: UUID
    user_update_data: User

    def build_request_context(self) -> RequestContext:
        return RequestContext(
            url_format={
                "user_id": str(self.user_id),
                "realm_name": self.realm_name,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
            body=self.user_update_data.serialize(),
        )
