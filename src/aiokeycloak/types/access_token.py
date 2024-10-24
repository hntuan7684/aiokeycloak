from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from adaptix import Retort, name_mapping

from aiokeycloak.types.base import FromResponse, KeycloakType


@dataclass(frozen=True, slots=True)
class AddressClaimSet(KeycloakType):
    country: str | None = None
    formatted: str | None = None
    locality: str | None = None
    postal_code: str | None = None
    region: str | None = None
    street_address: str | None = None


@dataclass(frozen=True, slots=True)
class Permission(KeycloakType):
    claims: dict[Any, Any] | None = None
    rsid: str | None = None
    rsname: str | None = None
    scopes: list[str] | None = None


@dataclass(frozen=True, slots=True)
class AccessTokenAuthorization(KeycloakType):
    permissions: list[Permission] | None = None


class CategoryType(str, Enum):
    INTERNAL = "internal"
    ACCESS = "access"
    ID = "id"
    ADMIN = "admin"
    USERINFO = "userinfo"
    LOGOUT = "logout"
    AUTHORIZATION_RESPONSE = "authorization_response"


@dataclass(frozen=True, slots=True)
class AccessTokenCertConf(KeycloakType):
    x5t: str | None = None


@dataclass(frozen=True, slots=True)
class AccessTokenAccess(KeycloakType):
    roles: list[str] | None = None
    verify_caller: bool | None = None


@dataclass(frozen=True, slots=True)
class AccessToken(KeycloakType):
    acr: str | None = None
    address: AddressClaimSet | None = None
    allowed_origins: list[str] | None = None
    at_hash: str | None = None
    auth_time: int | None = None
    authorization: AccessTokenAuthorization | None = None
    azp: str | None = None
    birthdate: str | None = None
    c_hash: str | None = None
    category: CategoryType | None = None
    claims_locales: str | None = None
    cnf: AccessTokenCertConf | None = None
    email: str | None = None
    email_verified: bool | None = None
    exp: int | None = None
    family_name: str | None = None
    gender: str | None = None
    given_name: str | None = None
    iat: int | None = None
    iss: str | None = None
    jti: str | None = None
    locale: str | None = None
    middle_name: str | None = None
    name: str | None = None
    nbf: int | None = None
    nickname: str | None = None
    nonce: str | None = None
    other_claims: dict[Any, Any] | None = None
    phone_number: str | None = None
    phone_number_verified: bool | None = None
    picture: str | None = None
    preferred_username: str | None = None
    profile: str | None = None
    realm_access: AccessTokenAccess | None = None
    s_hash: str | None = None
    scope: str | None = None
    session_state: str | None = None
    sid: str | None = None
    trusted_certs: list[str] | None = None
    typ: str | None = None
    updated_at: int | None = None
    website: str | None = None
    zone_info: str | None = None

    @classmethod
    def from_response(
        cls,
        data: FromResponse,
    ) -> AccessToken:
        return retort.load(data.body, cls)


retort = Retort(
    recipe=[
        name_mapping(
            AccessToken,
            map={
                "zone_info": "zoneinfo",
                "other_claims": "otherClaims",
                "trusted_certs": "trusted-certs",
                "allowed_origins": "allowed-origins",
            },
        ),
        name_mapping(
            AccessTokenCertConf,
            map={"x5t": ("cnf", "x5t#S256")},
        ),
    ],
)
