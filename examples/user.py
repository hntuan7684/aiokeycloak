import asyncio
from typing import Final, cast
from uuid import UUID

from aiokeycloak.client import KeycloakClient
from aiokeycloak.factory import KeycloakClientFactory
from aiokeycloak.sessions.aiohttp import AioHTTPKeycloakSession
from aiokeycloak.types.user import User

ACCESS_TOKEN_EXAMPLE: Final = "..."


async def methods_examples(client: KeycloakClient) -> None:
    users = await client.get_users("realm_name_example")
    created_user_id = await client.create_user(
        realm_name="realm_name_example",
        user=User(
            username="username_example",
            first_name="first_name_example",
            email="email_example",
            email_verified=False,
            enabled=True,
        ),
    )
    user = await client.get_user(
        realm_name="realm_name_example",
        user_id=created_user_id.user_id,
    )
    await client.update_user(
        realm_name="realm_name_example",
        user_id=cast(UUID, user.id),
        user_update_data=User(
            email_verified=True,
        ),
    )
    await client.delete_user(
        realm_name="realm_name_example",
        user_id=cast(UUID, user.id),
    )


async def main() -> None:
    async with KeycloakClientFactory(
        AioHTTPKeycloakSession("http://localhost:8081"),
    ) as factory:
        client = factory.factory(ACCESS_TOKEN_EXAMPLE)
        await methods_examples(client)


if __name__ == "__main__":
    asyncio.run(main())
