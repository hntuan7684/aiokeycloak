from abc import abstractmethod
from dataclasses import dataclass
from enum import auto, StrEnum
from typing import Any, Protocol, TypeVar

from aiokeyclock.types.base import KeycloakType


T = TypeVar('T', bound=KeycloakType)


class HTTPMethodType(StrEnum):
    GET = auto()
    PUT = auto()
    POST = auto()
    DELETE = auto()


@dataclass(frozen=True, slots=True)
class RequestContext:
    body: dict[str, Any] | None = None
    headers: dict[str, Any] | None = None
    url_format: dict[str, Any] | None = None
    query_parameters: dict[str, Any] | None = None


class KeycloakMethod(Protocol[T]):
    __url__: str
    __returning__: type[T]
    __http_method__: HTTPMethodType
    
    @abstractmethod
    def build_request_context(self) -> RequestContext:
        raise NotImplementedError
