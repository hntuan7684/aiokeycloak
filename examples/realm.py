import asyncio
from typing import Final
from uuid import UUID

from aiokeycloak.client import KeycloakClient
from aiokeycloak.factory import KeycloakClientFactory
from aiokeycloak.sessions.aiohttp import AioHTTPKeycloakSession


ACCESS_TOKEN_EXAMPLE: Final = "..."


async def methods_examples(client: KeycloakClient) -> None:
    realm = await client.get_realm("realm_name_example")
    realms_roles = await client.get_realms_roles("realm_name_example")
    await client.assign_realm_roles_to_user(
        realm_name="realm_name_example",
        user_id=UUID("user_uuid_id_example"),
        realm_roles_names=[realm.name],
    )


async def main() -> None:
    async with KeycloakClientFactory(
        AioHTTPKeycloakSession("http://localhost:8081"),
    ) as factory:
        client = factory.factory(ACCESS_TOKEN_EXAMPLE)
        await methods_examples(client)


if __name__ == "__main__":
    asyncio.run(main())
