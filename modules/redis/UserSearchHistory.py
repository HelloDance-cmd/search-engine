from modules.redis.Redis import RedisTemplate
from typing import List, Any


class SearchHistory(RedisTemplate):
    def __init__(self):
        super().__init__()

    def setUserSearchResult(self, user: str, keyword: str, result: List[str]) -> None:
        if result is None:
            return

        key = f"{user}:{keyword}"
        self.setList(key, result)

    def getUserSearchResult(self, user: str, keyword: str) -> List[str]:
        if user is None or keyword is None:
            return ['']

        key = f"{user}:{keyword}"
        lists = self.getList(key)

        return lists
