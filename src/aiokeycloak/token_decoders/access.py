import json
from typing import Any, Final

from jwcrypto import jwk, jwt


BEGIN_PUBLIC_KEY: Final = "-----BEGIN PUBLIC KEY-----\n"
END_PUBLIC_KEY: Final = "\n-----END PUBLIC KEY-----"


class AccessTokenDecoder:
    def __init__(self, access_token: str) -> None:
        self._access_token = access_token

    def decode(
        self, public_key: str, validate: bool = True, **kwargs: Any
    ) -> dict[str, Any]:
        if not validate:
            full_jwt = jwt.JWT(jwt=self._access_token, **kwargs)
            full_jwt.token.objects["valid"] = True
            return json.loads(full_jwt.token.payload.decode("utf-8"))

        if "key" not in kwargs:
            key = BEGIN_PUBLIC_KEY + public_key + END_PUBLIC_KEY
            key = jwk.JWK.from_pem(key.encode("utf-8"))
            kwargs["key"] = key

        key = kwargs.pop("key")
        leeway = kwargs.pop("leeway", 60)
        full_jwt = jwt.JWT(jwt=self._access_token, **kwargs)
        full_jwt.leeway = leeway
        full_jwt.validate(key)
        return jwt.json_decode(full_jwt.claims)
