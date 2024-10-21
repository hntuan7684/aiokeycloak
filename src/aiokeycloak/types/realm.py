from dataclasses import dataclass
from typing import Any

from adaptix import name_mapping, Retort

from aiokeycloak.types.base import KeycloakType

retort = Retort(
    recipe=[
        name_mapping(
            map={
                "name": "realm",
                "token_service": "token-service",
                "account_service": "account-service",
                "tokens_not_before": "tokens-not-before",
            },
        ),
    ],
)


@dataclass(frozen=True, slots=True)
class Realm(KeycloakType):
    name: str
    public_key: str
    token_service: str
    account_service: str
    tokens_not_before: int

    @classmethod
    def from_data(
        cls,
        data: Any,
    ) -> KeycloakType:
        return retort.load(data, cls)
