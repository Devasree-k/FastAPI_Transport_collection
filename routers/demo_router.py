
from fastapi import APIRouter, Cookie, Header, Request, Response

router = APIRouter(prefix="/demo", tags=["Headers, Cookies and Sessions"])


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


# 3. SESSIONS
@router.post("/session/last-viewed/{collection_id}")
async def remember_collection(
    collection_id: int,
    request: Request,
):
    request.session["last_viewed_collection_id"] = collection_id

    return {
        "message": "Collection ID saved in session",
        "collection_id": collection_id,
    }


@router.get("/session")
async def read_session(request: Request):
    return {
        "last_viewed_collection_id":
            request.session.get("last_viewed_collection_id")
    }


@router.post("/session/clear")
async def clear_session(request: Request):
    request.session.clear()
    return {"message": "Session cleared"}
