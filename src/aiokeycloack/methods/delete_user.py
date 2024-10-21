from dataclasses import dataclass
from uuid import UUID

from aiokeycloack.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeycloack.types.common import Success


@dataclass(frozen=True, slots=True)
class DeleteUser(KeycloakMethod[Success]):
    __url__ = "/admin/realms/{realm_name}/users/{user_id}"
    __returning__ = Success
    __http_method__ = HTTPMethodType.DELETE
    
    user_id: UUID
    realm_name: str
    access_token: str
    
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            url_format={
                'user_id': str(self.user_id),
                'realm_name': self.realm_name,
            },
        )
