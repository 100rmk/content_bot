from typing import Any, Union, Generator

import aioredis

from db.BaseModel import AsyncBaseCache


class AsyncRedisCache(AsyncBaseCache):
    def __init__(self, *, url: str):
        self.redis = aioredis.from_url(url, decode_responses=True)

    async def set(self, *, key: str, value: Union[str, bytes, int, float]):
        await self.redis.set(key, value)

    async def get(self, *, key: str):
        return await self.redis.get(key)

    async def delete(self, *, key: str):
        await self.redis.delete(key)
