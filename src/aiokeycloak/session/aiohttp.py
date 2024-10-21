from typing import (
    Any,
    TypeVar,
)

from aiohttp import ClientResponse, ClientSession, ContentTypeError

from aiokeycloak.methods.base import HTTPMethodType
from aiokeycloak.session.base import KeycloakSession, SendRequestDS


T = TypeVar("T")


class AioHTTPKeycloakSession(KeycloakSession):
    def __init__(
        self,
        server_url: str,
    ) -> None:
        self._client_session = ClientSession(server_url)

    async def _send_request(
        self,
        data: SendRequestDS,
    ) -> Any:
        if data.http_method == HTTPMethodType.GET:
            http_method = self._client_session.get
        elif data.http_method == HTTPMethodType.PUT:
            http_method = self._client_session.put
        elif data.http_method == HTTPMethodType.POST:
            http_method = self._client_session.post
        elif data.http_method == HTTPMethodType.DELETE:
            http_method = self._client_session.delete
        else:
            raise ValueError("Unknown http method %r" % data.http_method)

        response: ClientResponse
        async with http_method(
            url=data.url,
            data=data.body,
            headers=data.headers,
            params=data.query_parameters,
        ) as response:
            try:
                return await response.json(encoding="utf-8")
            except ContentTypeError:
                return {}

    async def close(self) -> None:
        await self._client_session.close()
