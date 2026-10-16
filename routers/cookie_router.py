
from fastapi import APIRouter, Cookie, Header, Request, Response

router = APIRouter(
    prefix="/demo", 
    tags=["Headers and Cookies"]
    )


# 1. HEADERS
@router.get("/headers")
async def read_headers(
    x_request_id: str | None = Header(default=None),
):
    return {
        "request_id": x_request_id,
        "message": "Header received",
    }


# 2. COOKIES
@router.post("/cookie")
async def set_cookie(response: Response):
    response.set_cookie(
        key="display_mode",
        value="dark",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600,
        path="/",
    )
    return {"message": "Display preference saved in cookie"}


@router.get("/cookie")
async def read_cookie(
    display_mode: str | None = Cookie(default=None),
):
    return {"display_mode": display_mode}


@router.delete("/cookie")
async def delete_cookie(response: Response):
    response.delete_cookie(
        key="display_mode",
        path="/",
    )
    return {"message": "Cookie deleted"}
