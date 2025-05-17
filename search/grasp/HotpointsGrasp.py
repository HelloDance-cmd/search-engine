"""
    新闻爬取工具
"""
from typing import List, Tuple

from bs4 import BeautifulSoup
from modules.models import Category, Website
from .Graps import Grasp
from .crawl_process.BaiduHotspotStrategy import BaiduHotspotStrategy
from .crawl_process.CCTVHotspotStrategy import CCTVHotspotStrategy
from .crawl_process.CrawlStrategyAbstract import CrawlStrategyAbstract
from .crawl_process.SinaHotspotStrategy import SinaHotspotStrategy
from .settings import URLS

from modules.Constant import CategoryConstant


class HotpotsNewGrasp(Grasp):
    def __init__(self):
        super().__init__()

        self.urls = URLS.copy()

    def start(self):
        """
            爬取热点信息
            存放到数据库中
        """
        for url in self.urls:
            self.url = self.urls[url]
            text = self.grasp()

            if url.find("sina") != -1:
                self.process(SinaHotspotStrategy(), text)
            elif url.find("cctv") != -1:
                # self.process(CCTVHotspotStrategy(), text)
                ...
            elif url.find("baidu") != -1:
                self.process(BaiduHotspotStrategy(), text)

    @staticmethod
    def add_to_mysql(url_and_title: List[Tuple[str, str, str]]):
        c = Category.objects.filter(name=CategoryConstant.HOTSPOT).first()
        if c is None:
            c = Category(name=CategoryConstant.HOTSPOT)
            c.save()

        if url_and_title.__len__() == 0:
            return

        for _, address, title in url_and_title:
            affect_rows = Website.objects.filter(address=address).values_list('id', flat=True).__len__()
            if affect_rows != 0:
                continue
            website = Website()
            website.address = address
            website.title = title
            website.categories = c

            # 由于是 ‘热点关键词’ 所以这两个都没有
            website.content = ''
            website.description = ''

            website.save()

    def process(self, processer: CrawlStrategyAbstract, html_text: str):
        result_set = processer.crawl_process(html_text)
        HotpotsNewGrasp.add_to_mysql(result_set)
