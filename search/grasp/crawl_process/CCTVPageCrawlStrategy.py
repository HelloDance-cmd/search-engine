from typing import List, Any

from bs4 import BeautifulSoup

from search.grasp.crawl_process.CrawlStrategyAbstract import CrawlStrategyAbstract


class CCTVPageCrawlStrategy(CrawlStrategyAbstract):
    def crawl_process(self, html_text: str) -> List[Any]:
        li_list = BeautifulSoup(html_text, "html.parser") \
            .find_all("li", class_="image")

        page_info_wrapper = []

        for li in li_list:
            official_name = "cctv"
            title = li.find("h3", class_="tit").get_text().strip()
            url = li.find("a").attrs["href"]
            text = li.find("p", class_="bre").get_text().strip()

            page_info_wrapper.append((official_name, url, title, text))
        return page_info_wrapper
