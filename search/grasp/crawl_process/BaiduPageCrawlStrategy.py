from typing import List, Any

from bs4 import BeautifulSoup

from search.grasp.crawl_process.CrawlStrategyAbstract import CrawlStrategyAbstract


class BaiduPageCrawlStrategy(CrawlStrategyAbstract):
    def crawl_process(self, html_text: str) -> List[Any]:
        div_boxes = BeautifulSoup(html_text, "html.parser") \
            .find_all("div", class_="result-op")

        page_info_wrapper = []
        for div_box in div_boxes:
            url = div_box.find("a").attrs["href"]
            title = div_box.find("h3").get_text().strip()
            text = div_box.find("div", class_="c-row").strip()
            official_name = "baidu"

            page_info_wrapper.append((official_name, url, title, text))

        return page_info_wrapper
