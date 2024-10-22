from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass
from typing import Any, cast, TypeVar

from aiokeycloak.errors import KeycloakError, KeycloakUnauthorizedError
from aiokeycloak.methods.base import HTTPMethodType, KeycloakMethod
from aiokeycloak.types.base import KeycloakType


T = TypeVar("T", bound=KeycloakType)


@dataclass(slots=True, frozen=True)
class RequestDS:
    url: str
    http_method: HTTPMethodType
    body: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    query_parameters: dict[str, str] | None = None


@dataclass(slots=True, frozen=True)
class ResponseDS:
    url: str
    body: Any
    http_status: int


def error_handling(response: ResponseDS) -> None:
    if not isinstance(response.body, dict):
        return None

    if "error" not in response.body:
        return None

    error = response.body["error"]
    error_description = response.body.get("error_description")

    if "Unauthorized" in error:
        raise KeycloakUnauthorizedError(
            "Unauthorized client. %r" % (error_description or error),
            raw_error=error,
            url=response.url,
            raw_body=response.body,
            http_status=response.http_status,
        )

    raise KeycloakError(
        (
            "An error has occurred. Url %r. %r."
            % (response.url, error_description or error)
        ),
        raw_error=error,
        url=response.url,
        raw_body=response.body,
        http_status=response.http_status,
    )


class KeycloakSession(Protocol):
    @abstractmethod
    async def _send_request(self, data: RequestDS) -> ResponseDS:
        raise NotImplementedError

    async def send_request(
        self,
        method: KeycloakMethod[T],
    ) -> T:
        request_context = method.build_request_context()
        print(request_context)
        send_request_ds = RequestDS(
            body=request_context.body,
            headers=request_context.headers,
            http_method=method.__http_method__,
            query_parameters=request_context.query_parameters,
            url=method.__url__.format_map(
                request_context.url_format or {},
            ),
        )
        data = await self._send_request(send_request_ds)
        error_handling(data)
        return cast(T, method.__returning__.from_data(data))

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
