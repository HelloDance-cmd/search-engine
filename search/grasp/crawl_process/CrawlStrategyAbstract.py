from abc import ABC, abstractmethod
from typing import List, Any


class CrawlStrategyAbstract(ABC):
    @abstractmethod
    def crawl_process(self, html_text: str) -> List[Any]: pass