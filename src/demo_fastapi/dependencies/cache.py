from collections.abc import Generator

from redis import Redis
from redis.backoff import NoBackoff
from redis.retry import Retry

from demo_fastapi.core.config import REDIS_URL


def get_redis() -> Generator[Redis | None]:
    if not REDIS_URL:
        yield None
        return

    client = Redis.from_url(
        REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=0.5,
        socket_timeout=0.5,
        retry=Retry(NoBackoff(), 0),
    )
    try:
        yield client
    finally:
        client.close()
