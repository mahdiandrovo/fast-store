import httpx

from fastapi import HTTPException, Request, Response

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}

async def forward_request(
    request: Request,
    client: httpx.AsyncClient,
    target_url: str,
    path: str,
) -> Response:

    url = f"{target_url.rstrip('/')}/{path.lstrip('/')}"

    if request.url.query:
        url = f"{url}?{request.url.query}"

    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in HOP_BY_HOP_HEADERS
    }

    body = await request.body()

    try:
        backend_response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Backend service timed out",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to backend service",
        )

    response_headers = {
        key: value
        for key, value in backend_response.headers.items()
        if key.lower() not in HOP_BY_HOP_HEADERS
    }

    return Response(
        content=backend_response.content,
        status_code=backend_response.status_code,
        headers=response_headers,
    )