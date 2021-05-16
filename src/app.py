from base64 import b64decode
from typing import Callable

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import UJSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from src import __version__
from src.routers import candles_router
from src.settings import AUTH_TOKEN, BASE_PATH, CHECK_AUTH_TOKEN, DEBUG, HOST, PORT, WORKERS

app = FastAPI(
    title="IqOption - Database",
    version=__version__,
    description="Database da IqOption",
    docs_url=f"{BASE_PATH}/docs",
    redoc_url=f"{BASE_PATH}/redoc",
    openapi_url=f"{BASE_PATH}/openapi.json",
)

app.include_router(candles_router, prefix=f"{BASE_PATH}/v1/candles")


@app.middleware("http")
async def check_auth(request: Request, call_next: Callable):
    if CHECK_AUTH_TOKEN and not b64decode(request.headers.get("X-Auth-Token", "").encode()).decode() == AUTH_TOKEN:
        raise HTTPException(HTTP_401_UNAUTHORIZED, {"message": "Invalid access token!"})

    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def unprocessable_entity_error(request, exc: RequestValidationError):
    return UJSONResponse(content={"message": exc.errors()}, status_code=HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(Exception)
async def unknown_error(request, exc: Exception):
    return UJSONResponse(content={"message": str(exc)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@app.exception_handler(HTTPException)
async def http_error(request, exc: HTTPException):
    return UJSONResponse(content={"message": exc.detail}, status_code=exc.status_code)


if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host=HOST,
        port=PORT,
        debug=DEBUG,
        log_level="info",
        access_log=True,
        workers=WORKERS,
        timeout_keep_alive=50,
    )
