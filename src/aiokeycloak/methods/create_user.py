from dataclasses import dataclass

from aiokeycloak.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeycloak.types.created_user_id import CreatedUserId
from aiokeycloak.types.user import User


@dataclass(frozen=True, slots=True)
class CreateUser(KeycloakMethod[CreatedUserId]):
    __url__ = "/admin/realms/{realm_name}/users"
    __returning__ = CreatedUserId
    __http_method__ = HTTPMethodType.POST

    realm_name: str
    access_token: str
    user: User

    def build_request_context(self) -> RequestContext:
        return RequestContext(
            body=self.user.serialize(),
            url_format={
                "realm_name": self.realm_name,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
        )
