from threading import Thread
from typing import List, Tuple
from urllib.parse import quote

from modules.Constant import CategoryConstant
from modules.models import Category, Website, User
from .Graps import Grasp
from .crawl_process.BaiduPageCrawlStrategy import BaiduPageCrawlStrategy
from .crawl_process.CCTVPageCrawlStrategy import CCTVPageCrawlStrategy
from .crawl_process.CrawlStrategyAbstract import CrawlStrategyAbstract
from .crawl_process.SinaPageCrawlStrategy import SinaPageCrawlStrategy


class GraspByKeywordNews(Grasp):

    def __init__(self, word: str, user_id: int):
        super().__init__()

        self.urls = {
            "sina": lambda k: f"https://search.sina.com.cn/?q={quote(k)}&c=news&from=channel&ie=utf-8",
            "cctv": lambda k, page=1: f"https://search.cctv.com/search.php?qtext={quote(k)}&type=web&page={page}",
            "baidu": lambda k, page=1: f"https://www.baidu.com/s?tn=news&ie=utf-8&word={quote(k)}&pn={(page - 1) * 10}"
        }

        # 请求的关键词
        self.word = word
        # 用户id
        self.user_id = user_id

    def start(self):
        category_not_exist = Category.objects.filter(name=CategoryConstant.NEWS).count() < 1
        if category_not_exist:
            category = Category(name=CategoryConstant.NEWS)
            category.save()

        self.grasp_by_keyword(self.word)

    def grasp_by_keyword(self, k, page=10):
        task_name_high_priority = 'sina'

        def remain_task():
            print('开始爬取')

            def crawl():
                for official_name in self.urls:
                    print(f'开启{official_name}')
                    # 如果是高优先级队伍这个应该已经完了
                    if official_name is task_name_high_priority:
                        continue

                    self.url = self.urls[official_name](k, cur_page)

                    html_str = self.grasp()
                    page_info_wra = None

                    if official_name.find("cctv") != -1:
                        # page_info_wra = self.parser(CCTVPageCrawlStrategy(), html_str)
                        ...
                    elif official_name.find("baidu") != -1:
                        page_info_wra = self.parser(BaiduPageCrawlStrategy(), html_str)

                    if page_info_wra:
                        self.add_to_mysql(page_info_wra)

            # 爬取1-page页的数据
            for cur_page in range(1, page + 1):  # 爬取10页数据
                Thread(target=crawl, args=()).start()

        # 默认参数不知道问什么没有效果，只能这样写
        page = 10 if page is None else page
        # 默认走新浪
        # 其余使用多线程完成
        self.url = self.urls[task_name_high_priority](k)
        sina_html = self.grasp()  # 默认通过url抓取

        page_info_wrapper = self.parser(SinaPageCrawlStrategy(), sina_html)
        if page_info_wrapper:
            self.add_to_mysql(page_info_wrapper)

        Thread(target=remain_task).start()

    def add_to_mysql(self, page_info_wrapper: List[Tuple[str, str, str, str]]):
        if not page_info_wrapper:
            return

        category = Category.objects.get(name=CategoryConstant.NEWS)
        if category is None:
            return
        category_id = category.id

        for page_info in page_info_wrapper:
            if len(page_info) != 4:
                continue

            _, address, title, text = page_info
            website = Website()
            website.title = title
            website.address = address
            website.description = text[:50]
            website.content = text
            website.categories = Category(pk=category_id)
            website.save()
            # 用户通过请求，请求过这个网站
            user = User.objects.get(pk=self.user_id)
            user.visited_website.add(website)

    def parser(self, processer: CrawlStrategyAbstract, html_text: str):
        return processer.crawl_process(html_text)