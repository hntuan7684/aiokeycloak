from __future__ import annotations

from dataclasses import dataclass

from aiokeycloak.types.base import FromResponse, KeycloakType
from aiokeycloak.types.user import User


@dataclass(frozen=True, slots=True)
class Users(KeycloakType):
    users: list[User]

    @classmethod
    def from_response(
        cls,
        data: FromResponse,
    ) -> Users:
        users = []
        for body in data.body:
            users.append(
                User.from_response(
                    FromResponse(
                        body=body,
                        headers=data.headers,
                    )
                ),
            )
        return cls(users=users)
