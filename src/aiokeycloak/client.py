from __future__ import annotations

from typing import Any, TypeVar
from uuid import UUID

from aiokeycloak.methods.base import KeycloakMethod
from aiokeycloak.methods.delete_user import DeleteUser
from aiokeycloak.methods.get_realm import GetRealm
from aiokeycloak.methods.get_realm_roles import GetRealmRoles
from aiokeycloak.session.base import KeycloakSession
from aiokeycloak.token_decoders.access import (
    AccessTokenDecoder,
)
from aiokeycloak.types.access_token import AccessToken
from aiokeycloak.types.base import KeycloakType
from aiokeycloak.types.realm import Realm
from aiokeycloak.types.realm_roles import RealmRoles


T = TypeVar("T", bound=KeycloakType)


class KeycloakClient:
    def __init__(
        self,
        access_token: str,
        session: KeycloakSession,
    ) -> None:
        self._session = session
        self._access_token = access_token

    async def send_request(self, method: KeycloakMethod[T]) -> T:
        return await self._session.send_request(method)

    async def get_realm(self, realm_name: str) -> Realm:
        method = GetRealm(realm_name=realm_name)
        return await self.send_request(method)

    async def get_realms_roles(
        self,
        realm_name: str,
        max: int | None = None,
        first: int | None = None,
        search: str | None = None,
        brief_representation: bool | None = None,
    ) -> RealmRoles:
        method = GetRealmRoles(
            realm_name=realm_name,
            max=max,
            first=first,
            search=search,
            access_token=self._access_token,
            brief_representation=brief_representation,
        )
        return await self.send_request(method)

    async def decode_access_token(
        self,
        realm_name: str,
        *,
        validate: bool = True,
        **kwargs: Any,
    ) -> AccessToken:
        access_token_decoder = AccessTokenDecoder(self._access_token)
        realm = await self.get_realm(realm_name)
        decode_access_token = access_token_decoder.decode(
            public_key=realm.public_key,
            validate=validate,
            **kwargs,
        )
        return AccessToken.from_data(decode_access_token)

    async def delete_user(
        self,
        user_id: UUID,
        realm_name: str,
    ) -> None:
        method = DeleteUser(
            user_id=user_id,
            realm_name=realm_name,
            access_token=self._access_token,
        )
        await self.send_request(method)
