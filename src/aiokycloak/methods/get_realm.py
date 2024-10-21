from dataclasses import dataclass

from aiokeycloack.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeycloack.types.realm import Realm


@dataclass(frozen=True, slots=True)
class GetRealm(KeycloakMethod[Realm]):
    __url__ = "/realms/{realm_name}"
    __returning__ = Realm
    __http_method__ = HTTPMethodType.GET
    
    realm_name: str
    
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            url_format={
                'realm_name': self.realm_name,
            },
        )