from typing import List, Any

from bs4 import BeautifulSoup

from search.grasp.crawl_process.CrawlStrategyAbstract import CrawlStrategyAbstract


class SinaPageCrawlStrategy(CrawlStrategyAbstract):
    def crawl_process(self, html_text: str) -> List[Any]:
        box_results = BeautifulSoup(html_text, "html.parser") \
            .find_all("div", class_="box-result")

        page_info_wrapper = []

        for box_result in box_results:
            a = box_result.find("a")
            p = box_result.find("p", class_="content")
            if a is None:
                continue

            official_name = "sina"
            url = a.attrs["href"]
            title = a.get_text().strip()
            text = "" if p is None else p.string.strip()

            page_info_wrapper.append((official_name, url, title, text))

        return page_info_wrapper
