# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from exceptions.transport_collection_exception import AppException
# from routers.driver_router import router as driver_router
# from routers.transport_collection_router import router as collection_router

# app = FastAPI(title="Transport Collection API")

# @app.exception_handler(AppException)
# async def app_exception_handler(request: Request, exc: AppException):
#     return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# app.include_router(driver_router)
# app.include_router(collection_router)

# @app.get("/")
# async def home():
#     return {"message": "Transport Collection API is running"}


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from config import SESSION_SECRET
from exceptions.transport_collection_exception import AppException
from routers.driver_router import router as driver_router
from routers.transport_collection_router import router as collection_router
from routers.demo_router import router as demo_router

if not SESSION_SECRET:
    raise RuntimeError("SESSION_SECRET must be configured in .env")

app = FastAPI(title="Transport Collection API")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=False,
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

app.include_router(driver_router)
app.include_router(collection_router)
app.include_router(demo_router)

@app.get("/")
async def home():
    return {"message": "Transport Collection API is running"}
