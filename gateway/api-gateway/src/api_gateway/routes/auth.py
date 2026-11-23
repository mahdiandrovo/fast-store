import httpx

from fastapi import APIRouter, Depends, Request

from api_gateway.config import USER_SERVICE_URL
from api_gateway.dependencies import get_http_client
from api_gateway.proxy import forward_request


router = APIRouter()


async def proxy_auth(
    request: Request,
    client: httpx.AsyncClient = Depends(get_http_client),
    path: str = "",
):
    return await forward_request(
        request=request,
        client=client,
        target_url=USER_SERVICE_URL,
        path=f"/api/v1/auth/{path}" if path else "/api/v1/auth",
    )


router.add_api_route(
    "",
    proxy_auth,
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)

router.add_api_route(
    "/{path:path}",
    proxy_auth,
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)