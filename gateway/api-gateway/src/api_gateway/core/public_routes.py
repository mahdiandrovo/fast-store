PUBLIC_ROUTES = {
    ("GET", "/"),
    ("GET", "/health"),
    ("POST", "/api/v1/auth/login"),
    ("POST", "/api/v1/users"),
}


def is_public_route(method: str, path: str) -> bool:
    return (method.upper(), path) in PUBLIC_ROUTES