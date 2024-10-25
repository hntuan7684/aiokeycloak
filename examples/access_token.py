import asyncio
from typing import Final

from aiokeycloak.factory import KeycloakClientFactory
from aiokeycloak.sessions.aiohttp import AioHTTPKeycloakSession

ACCESS_TOKEN_EXAMPLE: Final = "..."


async def main() -> None:
    async with KeycloakClientFactory(
        AioHTTPKeycloakSession("http://localhost:8081"),
    ) as factory:
        client = factory.factory(ACCESS_TOKEN_EXAMPLE)
        await client.decode_access_token(
            realm_name="realm_name_example",
            validate=False,
        )


if __name__ == "__main__":
    asyncio.run(main())
