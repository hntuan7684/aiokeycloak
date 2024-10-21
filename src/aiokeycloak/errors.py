from dataclasses import dataclass
from typing import Any


@dataclass
class KeycloakError(Exception):
    msg: str
    body: Any
    url: str
    raw_error: Any
    http_status: int
