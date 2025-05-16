from typing import List, Any

from bs4 import BeautifulSoup

from search.grasp.crawl_process.CrawlStrategyAbstract import CrawlStrategyAbstract


class CCTVHotspotStrategy(CrawlStrategyAbstract):
    def crawl_process(self, html_text: str) -> List[Any]:
        li_list = BeautifulSoup(html_text, "html.parser") \
            .find("ul", id="newslist") \
            .find_all("li")

        url_and_title = []

        for li in li_list:
            a = li.find("a")
            url = a.attrs["href"]
            title = a.string.strip()
            url_and_title.append(("sina", url, title))

        return url_and_title