from dataclasses import dataclass
from uuid import UUID

from aiokeycloak.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeycloak.types.user import User


@dataclass(frozen=True, slots=True)
class GetUser(KeycloakMethod[User]):
    __url__ = "/admin/realms/{realm_name}/users/{user_id}"
    __returning__ = User
    __http_method__ = HTTPMethodType.GET

    access_token: str
    realm_name: str

    user_id: UUID

    def build_request_context(self) -> RequestContext:
        return RequestContext(
            url_format={
                "user_id": self.user_id,
                "realm_name": self.realm_name,
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
            },
        )
