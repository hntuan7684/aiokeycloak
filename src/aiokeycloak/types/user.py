from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from adaptix import name_mapping, NameStyle, Retort

from aiokeycloak.types.base import KeycloakType


@dataclass(frozen=True, slots=True)
class UserProfileAttributeMetadata(KeycloakType):
    name: str | None = None
    display_name: str | None = None
    optional: bool | None = None
    read_only: bool | None = None
    annotations: dict[str, Any] | None = None
    validators: dict[str, dict[str, Any]] | None = None
    group: str | None = None
    multivalued: bool | None = None

    @classmethod
    def from_data(
        cls,
        data: Any,
    ) -> UserProfileAttributeMetadata:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class UserProfileAttributeGroupMetadata(KeycloakType):
    name: str | None = None
    display_header: str | None = None
    display_description: str | None = None
    annotations: dict[str, Any] | None = None

    @classmethod
    def from_data(
        cls,
        data: Any,
    ) -> UserProfileMetadata:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class UserProfileMetadata(KeycloakType):
    attributes: list[UserProfileAttributeMetadata] | None = None
    groups: list[UserProfileAttributeGroupMetadata] | None = None

    @classmethod
    def from_data(
        cls,
        data: Any,
    ) -> UserProfileMetadata:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class User(KeycloakType):
    id: UUID | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    email_verified: bool | None = None
    attributes: dict[str, list[Any]] | None = None
    user_profile_metadata: UserProfileMetadata | None = None
    self: str | None = None
    origin: str | None = None
    created_timestamp: int | None = None
    enabled: bool | None = None
    totp: bool | None = None
    federation_link: str | None = None
    service_account_client_id: str | None = None
    credentials: dict[str, Any] | None = None
    disableable_credential_types: set[str] | None = None
    required_actions: list[str] | None = None
    realm_roles: list[str] | None = None
    client_roles: dict[str, list[Any]] | None = None
    not_before: int | None = None
    application_roles: dict[str, list[Any]] | None = None
    groups: list[str] | None = None
    access: dict[str, bool] | None = None

    @classmethod
    def from_data(
        cls,
        data: dict[str, str],
    ) -> User:
        return retort.load(data, cls)


retort = Retort(
    recipe=[
        name_mapping(
            UserProfileAttributeMetadata,
            name_style=NameStyle.CAMEL,
        ),
        name_mapping(
            User,
            name_style=NameStyle.CAMEL,
        ),
        name_mapping(
            UserProfileAttributeGroupMetadata,
            name_style=NameStyle.CAMEL,
        ),
    ],
)
