from abc import abstractmethod
from asyncio import Protocol
from dataclasses import dataclass
from typing import Any, cast, TypeVar

from aiokeycloak.errors import (
    KeycloakError,
    UnauthorizedError,
    UserExistsError,
)
from aiokeycloak.methods.base import HTTPMethodType, KeycloakMethod
from aiokeycloak.types.base import FromResponse, KeycloakType


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
    headers: dict[str, Any]


def error_handling(response: ResponseDS) -> None:
    if not isinstance(response.body, dict):
        return None

    if response.http_status < 400:
        return None

    error: str = (
        response.body.get("error")
        or response.body.get("error_description")
        or response.body.get("errorMessage")
        or ""
    )
    error_data: dict[str, Any] = {
        "raw_error": error,
        "url": response.url,
        "raw_body": response.body,
        "http_status": response.http_status,
    }
    if "Unauthorized" in error:
        raise UnauthorizedError(
            "Unauthorized client. %s" % error,
            **error_data,
        )

    if "User exists" in error:
        raise UserExistsError(error, **error_data)

    raise KeycloakError(
        "An error has occurred. Url %r. %r." % (response.url, error),
        **error_data,
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
        returning = method.__returning__.from_response(
            FromResponse(
                body=data.body,
                headers=data.headers,
            ),
        )
        return cast(T, returning)

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
