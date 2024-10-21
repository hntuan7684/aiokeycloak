from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiokeycloak.types.base import KeycloakType
from aiokeycloak.types.user import User


@dataclass(frozen=True, slots=True)
class Users(KeycloakType):
    users: list[User]

    @classmethod
    def from_data(
        cls,
        data: list[dict[str, Any]],
    ) -> Users:
        users = []
        for datum in data:
            users.append(User.from_data(datum))
        return cls(users=users)
