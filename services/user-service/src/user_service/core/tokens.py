from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import jwt

from user_service.core.config import settings


# Load the RSA private key
private_key = Path(settings.JWT_PRIVATE_KEY_PATH).read_text(
    encoding="utf-8"
)


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "exp": expires_at,
        "jti": uuid4().hex,
        "type": "access",
    }

    token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
    )

    return token

public_key = Path(settings.JWT_PUBLIC_KEY_PATH).read_text(
    encoding="utf-8"
)

def verify_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        issuer=settings.JWT_ISSUER,
        audience=settings.JWT_AUDIENCE,
    )

    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Invalid token type.")

    return payload