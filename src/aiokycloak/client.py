from __future__ import annotations

from types import TracebackType
from typing import Any, TypeVar
from uuid import UUID

from aiokeycloack.methods.base import KeycloakMethod
from aiokeycloack.methods.delete_user import DeleteUser
from aiokeycloack.methods.get_realm import GetRealm
from aiokeycloack.methods.get_realm_roles import GetRealmRoles
from aiokeycloack.session.aiohttp import AioHTTPKeycloakSession
from aiokeycloack.session.base import KeycloakSession
from aiokeycloack.token_decoders.access import (
    AccessTokenDecoder,
)
from aiokeycloack.types.access_token import AccessToken
from aiokeycloack.types.base import KeycloakType
from aiokeycloack.types.realm import Realm
from aiokeycloack.types.realm_roles import RealmRoles


T = TypeVar('T', bound=KeycloakType)


class KeycloakClient:
    def __init__(self, session: KeycloakSession) -> None:
        self._session = session
    
    async def send_request(self, method: KeycloakMethod[T]) -> T:
        return await self._session.send_request(method)
    
    async def __aenter__(self) -> KeycloakClient:
        return self
    
    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        await self.close()
    
    async def get_realm(self, realm_name: str) -> Realm:
        method = GetRealm(realm_name=realm_name)
        return await self.send_request(method)
    
    async def get_realms_roles(
        self,
        realm_name: str,
        access_token: str,
        max: int | None = None,
        first: int | None = None,
        search: str | None = None,
        brief_representation: bool | None = None,
    ) -> RealmRoles:
        method = GetRealmRoles(
            realm_name=realm_name,
            access_token=access_token,
            max=max,
            first=first,
            search=search,
            brief_representation=brief_representation,
        )
        return await self.send_request(method)
    
    async def decode_access_token(
        self,
        access_token: str,
        realm_name: str,
        *,
        validate: bool = True,
        **kwargs: Any,
    ) -> AccessToken:
        access_token_decoder = AccessTokenDecoder(access_token)
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
        access_token: str,
    ) -> None:
        method = DeleteUser(
            user_id=user_id,
            realm_name=realm_name,
            access_token=access_token,
        )
        await self.send_request(method)
    
    async def close(self) -> None:
        await self._session.close()


def aiokeycloack(
    server_url: str,
    session: KeycloakSession | None = None
) -> KeycloakClient:
    if session is None:
        session = AioHTTPKeycloakSession(server_url)
    return KeycloakClient(session)
