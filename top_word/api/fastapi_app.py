import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from top_word.api.api import router
from top_word.common import connect_to_redis
from top_word.exception_handlers import common_exception_handler

api_host = os.getenv("API_HOST", "0.0.0.0")
api_port = int(os.getenv("API_PORT", 8000))
logger = logging.getLogger("fastapi_app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis_client = await connect_to_redis()
    logger.info("Connected to Redis")
    app.state.redis_client = redis_client
    yield


def create_fastapi_app() -> FastAPI:
    app = FastAPI(
        title="Word of the Day",
        description="Serves the topic for the word of the day",
        version="1.0.0.",
        lifespan=lifespan,
    )

    app.include_router(router)
    app.add_exception_handler(RequestValidationError, common_exception_handler)
    app.add_exception_handler(StarletteHTTPException, common_exception_handler)
    app.add_exception_handler(Exception, common_exception_handler)

    return app


app = create_fastapi_app()


def start_rest_api() -> None:
    uvicorn.run(app, host=api_host, port=api_port)


if __name__ == "__main__":
    start_rest_api()
