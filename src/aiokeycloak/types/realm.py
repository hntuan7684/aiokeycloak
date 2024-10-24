from dataclasses import dataclass

from adaptix import Retort, name_mapping

from aiokeycloak.types.base import FromResponse, KeycloakType

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
    def from_response(
        cls,
        data: FromResponse,
    ) -> KeycloakType:
        return retort.load(data.body, cls)
