from dataclasses import dataclass
from uuid import UUID

from aiokeyclock.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeyclock.types.user_representation import UserRepresentation


@dataclass(frozen=True, slots=True)
class GetUser(KeycloakMethod[UserRepresentation]):
    __url__ = '/admin/realms/{realm_name}/users/{user_id}'
    __returning__ = UserRepresentation
    __http_method__ = HTTPMethodType.GET
    
    user_id: UUID
    realm_name: str
    
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            url_format={
                'user_id': self.user_id,
                'realm_name': self.realm_name,
            },
        )
