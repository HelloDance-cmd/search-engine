"""
    新闻爬取工具
"""
from typing import List, Tuple

from bs4 import BeautifulSoup
from modules.models import Category, Website
from .Graps import Grasp
from .settings import URLS


class HotpointsNewGrasp(Grasp):
    def __init__(self):
        super().__init__()

        self.urls = URLS.copy()

    def news_hot_points_grasp(self):
        """
            爬取热点信息
            存放到数据库中
        """
        for url in self.urls:
            self.url = self.urls[url]
            text = self.grasp()

            if url.find("sina") != -1:
                HotpointsNewGrasp.sina_grasp(text)
            elif url.find("cctv") != -1:
                HotpointsNewGrasp.cctv_grasp(text)
            elif url.find("baidu") != -1:
                HotpointsNewGrasp.baidu_grasp(text)

    @staticmethod
    def add_to_mysql(url_and_title: List[Tuple[str, str, str]]):
        # (official_name, url, title)
        if url_and_title.__len__() == 0:
            return
        
        for _, address, title in url_and_title:
            affect_rows = Website.objects.filter(address=address).values_list('id', flat=True).__len__()
            if affect_rows != 0:
                continue
            website = Website()
            website.address = address
            website.title = title
            website.categories = Category(pk=1)

            # 由于是 ‘热点关键词’ 所以这两个都没有
            website.content = ''
            website.description = ''

            website.save()

    @staticmethod
    def sina_grasp(html: str) -> None:
        li_list = BeautifulSoup(html, "html.parser") \
            .find("div", class_="blk_main_li") \
            .find_all("li")

        url_and_title = []

        for li in li_list:
            a = li.find("a")
            url = a.attrs["href"]
            title = a.string.strip()
            url_and_title.append(("sina", url, title))

        HotpointsNewGrasp.add_to_mysql(url_and_title)

    @staticmethod
    def cctv_grasp(html: str) -> None:
        li_list = BeautifulSoup(html, "html.parser") \
            .find("ul", id="newslist") \
            .find_all("li")

        url_and_title = []

        for li in li_list:
            a = li.find("a")
            url = a.attrs["href"]
            title = a.string.strip()
            url_and_title.append(("sina", url, title))

        HotpointsNewGrasp.add_to_mysql(url_and_title)

    @staticmethod
    def baidu_grasp(html: str) -> None:
        elements = BeautifulSoup(html, "html.parser") \
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

        HotpointsNewGrasp.add_to_mysql(url_and_title)
