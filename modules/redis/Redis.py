from typing import Any, List
import redis

_default_config = {"host": "localhost", "port": 6379, "db": 1, "encoding": "UTF-8",
                   "charset": 'UTF-8', "decode_responses": True}


class RedisTemplate:
    _redisClient = None

    def __init__(self, redis_conf=_default_config, exp_mins=30):
        self._redisClient = redis.StrictRedis(**redis_conf)
        self.exp_seconds = exp_mins * 60

    def set(self, key: str, name: str) -> None:
        self._redisClient.set(key, name, ex=self.exp_seconds, nx=True)

    def setList(self, key: str, values: List[str]):
        for value in values:
            self._redisClient.lpush(key, value)

        self._redisClient.expire(key, time=self.exp_seconds)

    def exists(self, key: str):
        return self._redisClient.exists(key)

    def getList(self, key: str) -> List[Any]:
        return self._redisClient.lrange(key, 0, -1)

    def setExpire(self, key: str, exp_mins: int):
        exp_seconds = exp_mins * 60
        self._redisClient.expire(key, time=exp_seconds)
