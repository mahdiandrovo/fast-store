import httpx

from fastapi import APIRouter, Depends, Request

from api_gateway.config import PRODUCT_SERVICE_URL
from api_gateway.dependencies import get_http_client
from api_gateway.proxy import forward_request


router = APIRouter()


async def proxy_prodcuts(
    request: Request,
    client: httpx.AsyncClient = Depends(get_http_client),
    path: str = "",
):
    return await forward_request(
        request=request,
        client=client,
        target_url=PRODUCT_SERVICE_URL,
        path=f"/api/v1/products/{path}" if path else "/api/v1/products",
    )


router.add_api_route(
    "",
    proxy_prodcuts,
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)

router.add_api_route(
    "/{path:path}",
    proxy_prodcuts,
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)