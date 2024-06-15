import redis

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.CACHE_HOST,
            port=settings.CACHE_PORT,
            db=settings.CACHE_DB,
        )

    def set_message(self, key: str, message: str) -> None:
        self.client.set(key, message)

    def get_message(self, key: str) -> str:
        message = self.client.get(key)
        return message.decode("utf-8") if message else None


redis_client = RedisClient()
