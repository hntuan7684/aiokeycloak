from __future__ import annotations

from types import TracebackType

from aiokeycloak.client import KeycloakClient
from aiokeycloak.session.aiohttp import AioHTTPKeycloakSession
from aiokeycloak.session.base import KeycloakSession


class KeycloakClientFactory:
    def __init__(
        self,
        server_url: str,
        session: KeycloakSession | None = None,
    ) -> None:
        if session is None:
            session = AioHTTPKeycloakSession(server_url)
        self._session = session

    async def __aenter__(self) -> KeycloakClientFactory:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        await self.close()

    def factory(self, access_token: str) -> KeycloakClient:
        return KeycloakClient(
            session=self._session,
            access_token=access_token,
        )

    async def close(self) -> None:
        await self._session.close()
