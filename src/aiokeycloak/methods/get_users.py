from dataclasses import dataclass

from aiokeycloak.methods.base import (
    HTTPMethodType,
    KeycloakMethod,
    RequestContext,
)
from aiokeycloak.types.users import Users


@dataclass(frozen=True, slots=True)
class GetUsers(KeycloakMethod[Users]):
    __url__ = "/admin/realms/{realm_name}/users"
    __returning__ = Users
    __http_method__ = HTTPMethodType.GET

    realm_name: str
    access_token: str

    brief_representation: bool | None = None
    email: str | None = None
    email_verified: bool | None = None
    enabled: bool | None = None
    exact: bool | None = None
    first: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    max: int | None = None
    username: str | None = None

    def build_request_context(self) -> RequestContext:
        query_parameters = [
            ("briefRepresentation", self.brief_representation),
            ("email", self.email),
            ("emailVerified", self.email_verified),
            ("enabled", self.enabled),
            ("exact", self.exact),
            ("first", self.first),
            ("firstName", self.first_name),
            ("lastName", self.last_name),
            ("max", self.max),
            ("username", self.username),
        ]

        return RequestContext(
            url_format={
                "realm_name": self.realm_name,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            },
            query_parameters={
                data[0]: data[1] for data in query_parameters if data[1]
            },
        )
