from typing import Any, List

from bs4 import BeautifulSoup

from search.grasp.crawl_process.CrawlStrategyAbstract import CrawlStrategyAbstract


class SinaHotspotStrategy(CrawlStrategyAbstract):
    def crawl_process(self, html_text: str) -> List[Any]:
        li_list = BeautifulSoup(html_text, "html.parser") \
            .find("div", class_="blk_main_li") \
            .find_all("li")

        url_and_title = []

        for li in li_list:
            a = li.find("a")
            url = a.attrs["href"]
            title = a.string.strip()
            url_and_title.append(("sina", url, title))

        return url_and_title