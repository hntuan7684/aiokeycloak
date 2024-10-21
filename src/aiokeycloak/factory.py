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

    def factory(self, access_token: str) -> KeycloakClient:
        return KeycloakClient(
            session=self._session,
            access_token=access_token,
        )

    async def close(self) -> None:
        await self._session.close()
