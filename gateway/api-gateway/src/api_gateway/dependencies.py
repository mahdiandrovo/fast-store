import logging

import httpx

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from jwt import InvalidTokenError

from api_gateway.core.public_routes import is_public_route
from api_gateway.core.security import verify_access_token

logger = logging.getLogger("api_gateway.auth")


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

bearer_scheme = HTTPBearer(auto_error=False)


async def authenticate_request(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    if is_public_route(request.method, request.url.path):
        logger.info(
            "Public request: %s %s",
            request.method,
            request.url.path,
        )
        return None

    if credentials is None:

        logger.info(
            "Authentication required: %s %s",
            request.method,
            request.url.path,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = verify_access_token(credentials.credentials)

        logger.info(
            "JWT authentication successful: %s %s",
            request.method,
            request.url.path,
        )

        return payload

    except InvalidTokenError:

        logger.warning(
            "JWT authentication failed: %s %s",
            request.method,
            request.url.path,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )