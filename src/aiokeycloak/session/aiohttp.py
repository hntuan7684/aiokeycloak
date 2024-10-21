from abc import abstractmethod
from typing import Protocol, Unpack

from aiohttp import ClientSession
from aiohttp.client import _RequestContextManager, _RequestOptions
from aiohttp.typedefs import StrOrURL

from aiokeycloak.methods.base import HTTPMethodType
from aiokeycloak.session.base import KeycloakSession, RequestDS, ResponseDS


class AioHTTPMethod(Protocol):
    @abstractmethod
    def __call__(
        self,
        url: StrOrURL,
        **kwargs: Unpack[_RequestOptions],
    ) -> _RequestContextManager:
        raise NotImplementedError


class AioHTTPKeycloakSession(KeycloakSession):
    def __init__(
        self,
        server_url: str,
    ) -> None:
        self._client_session = ClientSession(server_url)

    def _load_http_method(self, http_method: HTTPMethodType) -> AioHTTPMethod:
        if http_method == HTTPMethodType.GET:
            return self._client_session.get
        elif http_method == HTTPMethodType.PUT:
            return self._client_session.put
        elif http_method == HTTPMethodType.POST:
            return self._client_session.post
        elif http_method == HTTPMethodType.DELETE:
            return self._client_session.delete
        else:
            raise ValueError("Unknown http method %r" % http_method)

    async def _send_request(
        self,
        request: RequestDS,
    ) -> ResponseDS:
        http_method = self._load_http_method(request.http_method)
        async with http_method(
            url=request.url,
            data=request.body,
            headers=request.headers,
            params=request.query_parameters,
        ) as response:
            if response.status == 204:
                body = {}
            else:
                body = await response.json(encoding="utf-8")

            return ResponseDS(
                body=body,
                url=request.url,
                http_status=response.status,
            )

    async def close(self) -> None:
        await self._client_session.close()
