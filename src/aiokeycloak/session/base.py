from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass
from typing import Any, TypeVar

from aiokeycloak.methods.base import HTTPMethodType, KeycloakMethod
from aiokeycloak.types.base import KeycloakType


T = TypeVar('T', bound=KeycloakType)


@dataclass(slots=True, frozen=True)
class SendRequestDS:
    url: str
    http_method: HTTPMethodType
    body: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    query_parameters: dict[str, str] | None = None


# TODO: сделать обработку ошибок
class KeycloakSession(Protocol):
    @abstractmethod
    async def _send_request(self, data: SendRequestDS) -> Any:
        raise NotImplementedError
    
    async def send_request(
        self,
        method: KeycloakMethod[T],
    ) -> T:
        request_context = method.build_request_context()
        send_request_ds = SendRequestDS(
            body=request_context.body,
            headers=request_context.headers,
            http_method=method.__http_method__,
            query_parameters=request_context.query_parameters,
            url=method.__url__.format_map(
                request_context.url_format or {},
            ),
        )
        data = await self._send_request(send_request_ds)
        return method.__returning__.from_data(data)
    
    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
