from typing import List, Any

from bs4 import BeautifulSoup
from search.grasp.crawl_process.CrawlStrategyAbstract import CrawlStrategyAbstract


class BaiduHotspotStrategy(CrawlStrategyAbstract):
    def crawl_process(self, html_text: str) -> List[Any]:
        elements = BeautifulSoup(html_text, "html.parser") \
            .find("div", id="pane-news") \
            .find_all(["div", "ul"])

        url_and_title = []

        for element in elements:
            a = element.find("a")

            if a is None:
                continue

            url = a.attrs["href"]
            title = a.string.strip()
            url_and_title.append(("cctv", url, title))

        return url_and_title
