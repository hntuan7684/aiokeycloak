from abc import abstractmethod
from typing import Any, Protocol, cast

from aiohttp import ClientSession, ContentTypeError
from aiohttp.client import _RequestContextManager
from aiohttp.typedefs import StrOrURL

from aiokeycloak.methods.base import HTTPMethodType
from aiokeycloak.sessions.base import KeycloakSession, RequestDS, ResponseDS


class AioHTTPMethod(Protocol):
    @abstractmethod
    def __call__(
        self,
        url: StrOrURL,
        **kwargs: Any,
    ) -> _RequestContextManager:
        raise NotImplementedError


class AioHTTPKeycloakSession(KeycloakSession):
    def __init__(
        self,
        server_url: str,
    ) -> None:
        self._client_session = ClientSession(server_url)

    def _load_http_method(self, http_method: HTTPMethodType) -> AioHTTPMethod:
        method: Any
        if http_method == HTTPMethodType.GET:
            method = self._client_session.get
        elif http_method == HTTPMethodType.PUT:
            method = self._client_session.put
        elif http_method == HTTPMethodType.POST:
            method = self._client_session.post
        elif http_method == HTTPMethodType.DELETE:
            method = self._client_session.delete
        else:
            msg = f"Unknown http method {http_method!r}"
            raise ValueError(msg)
        return cast(AioHTTPMethod, method)

    async def _send_request(
        self,
        request: RequestDS,
    ) -> ResponseDS:
        http_method = self._load_http_method(request.http_method)
        async with http_method(
            url=request.url,
            json=request.body,
            headers=request.headers,
            params=request.query_parameters,
        ) as response:
            try:
                body = await response.json(encoding="utf-8")
            except ContentTypeError:
                body = (await response.read()).decode(encoding="utf-8")

            return ResponseDS(
                body=body,
                url=request.url,
                http_status=response.status,
                headers=dict(response.headers),
            )

    async def close(self) -> None:
        await self._client_session.close()
