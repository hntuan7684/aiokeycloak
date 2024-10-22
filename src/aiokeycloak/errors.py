from dataclasses import dataclass
from typing import Any


@dataclass
class KeycloakError(Exception):
    msg: str
    url: str
    raw_body: Any
    raw_error: Any
    http_status: int


@dataclass
class UnauthorizedError(KeycloakError):
    pass


@dataclass
class UserExistsError(KeycloakError):
    pass
