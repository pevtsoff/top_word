import asyncio
import logging
import os
from functools import wraps
from typing import Any, Callable

import redis as sync_redis
import redis.asyncio as redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError
from redis.exceptions import TimeoutError as redisTimeoutError

LOG_FORMAT = os.getenv(
    "LOG_FORMAT",
    "%(asctime)-15s %(name)s [%(levelname)s] %(filename)s:%(lineno)d  %(message)s",
)
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
retry = Retry(ExponentialBackoff(), 3)


def configure_logger(name: str, log_level: str = LOG_LEVEL) -> logging.Logger:
    logging.basicConfig(format=LOG_FORMAT)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    return logger


logger = configure_logger(__name__)


async def repeat(interval: int, func: Callable, *args: tuple, **kwargs: dict) -> None:
    while True:
        func_name = func.__name__
        logger.warning(f"Creating periodic task '{func_name}'")

        try:
            await func(*args, **kwargs)

        except Exception as e:
            logger.exception(f"Error running {func_name}: {e}")

        await asyncio.sleep(int(interval))


async def connect_to_redis() -> Any:
    try:
        redis_client = await redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            retry=retry,
            retry_on_error=[BusyLoadingError, ConnectionError, redisTimeoutError],
        )

        await redis_client.ping()

    except sync_redis.exceptions.ConnectionError:
        logger.exception("Cant connect to redis at this moment, " "will be retrying on the next flush attempt")
        raise

    return redis_client


async def flush_data_to_redis(key: str, data: str) -> None:
    redis_client = await connect_to_redis()
    logger.info("Flushing  data of the day to redis with key %s - %s ", key, data)
    await redis_client.set(key, str(data))


def with_retry(exceptions: Any, attempts: int = 5, delay: int = 1, backoff: int = 2) -> Callable:
    """
    Retry decorator with exponential backoff.

    :param exceptions: Exception(s) to check
    :param attempts: Number of attempts before giving up
    :param delay: Initial delay between attempts
    :param backoff: Multiplier applied to delay between attempts
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        async def wrapper(*args: list, **kwargs: dict) -> Any:
            attempt = 1
            current_delay = delay
            while attempt <= attempts:
                try:
                    return await f(*args, **kwargs)

                except exceptions as e:
                    if attempt == attempts:
                        raise
                    logger.info(f"Attempt {attempt} failed: {e}. Retrying in {current_delay} seconds...")

                    await asyncio.sleep(current_delay)

                    attempt += 1
                    current_delay *= backoff

        return wrapper

    return decorator
