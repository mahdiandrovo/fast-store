from pathlib import Path

import jwt
from jwt import InvalidTokenError

from api_gateway.config import (
    JWT_AUDIENCE,
    JWT_ISSUER,
    JWT_PUBLIC_KEY_PATH,
)

def load_public_key() -> str:
    public_key_path = Path(JWT_PUBLIC_KEY_PATH)

    if not public_key_path.exists():
        raise RuntimeError(
            f"JWT public key not found: {public_key_path}"
        )

    return public_key_path.read_text(encoding="utf-8")

def verify_access_token(token: str) -> dict:
    public_key = load_public_key()

    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        issuer=JWT_ISSUER,
        audience=JWT_AUDIENCE,
        options={
            "require": [
                "exp",
                "iat",
                "sub",
                "jti",
            ]
        },
    )

    if payload.get("type") != "access":
        raise InvalidTokenError("Invalid token type")

    return payload