from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions.transport_collection_exception import AppException
from routers.driver_router import router as driver_router
from routers.transport_collection_router import router as collection_router

app = FastAPI(title="Transport Collection API")

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(driver_router)
app.include_router(collection_router)

@app.get("/")
async def home():
    return {"message": "Transport Collection API is running"}
