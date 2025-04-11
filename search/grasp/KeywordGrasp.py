from threading import Thread
from typing import List, Tuple
from urllib.parse import quote
from bs4 import BeautifulSoup

from modules.models import Category, Website, User
from modules.Constant import CategoryConstant

from .Graps import Grasp


class GraspByKeywordNews(Grasp):
    CATEGORY = CategoryConstant.NEWS

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
        category_is_exist = Category.objects.filter(name=self.CATEGORY).count() >= 1
        if not category_is_exist:
            category = Category(name=self.CATEGORY)
            category.save()

        self.grasp_by_keyword(self.word)

    def grasp_by_keyword(self, k, page=10):
        task_name_high_priority = 'sina'
        def remain_task():
            # 爬取1-page页的数据
            for cur_page in range(1, page + 1):  # 爬取10页数据
                for official_name in self.urls:

                    # 如果是高优先级队伍这个应该已经完了
                    if official_name is task_name_high_priority:
                        continue

                    self.url = self.urls[official_name](k, cur_page)

                    sina_html = self.grasp()
                    page_info_wrapper = None

                    if official_name.find("cctv") != -1:
                        page_info_wrapper = GraspByKeywordNews.cctv_parse(sina_html)
                    elif official_name.find("baidu") != -1:
                        page_info_wrapper = GraspByKeywordNews.baidu_parse(sina_html)

                    if page_info_wrapper:
                        GraspByKeywordNews.add_to_mysql(page_info_wrapper, k)

        # 默认参数不知道问什么没有效果，只能这样写
        page = 10 if page is None else page
        # 默认走新浪
        # 其余使用多线程完成
        self.url = self.urls[task_name_high_priority](k)
        sina_html = self.grasp()  # 默认通过url抓取
        page_info_wrapper = GraspByKeywordNews.sina_parse(sina_html)
        if page_info_wrapper:
            self.add_to_mysql(page_info_wrapper)

        Thread(target=remain_task).start()


    def add_to_mysql(self, page_info_wrapper: List[Tuple[str, str, str, str]]):
        if not page_info_wrapper:
            return

        category = Category.objects.get(name=GraspByKeywordNews.CATEGORY)
        if category is None:
            return
        category_id = category.id
        for _, address, title, text in page_info_wrapper:
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

    @staticmethod
    def sina_parse(html: str):
        box_results = BeautifulSoup(html, "html.parser") \
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

    @staticmethod
    def cctv_parse(html: str):
        #  official_name, url, title, text
        li_list = BeautifulSoup(html, "html.parser") \
            .find_all("li", class_="image")

        page_info_wrapper = []

        for li in li_list:
            official_name = "cctv"
            title = li.find("h3", class_="tit").get_text().strip()
            url = li.find("a").attrs["href"]
            text = li.find("p", class_="bre").get_text().strip()

            page_info_wrapper.append((official_name, url, title, text))
        return page_info_wrapper

    @staticmethod
    def baidu_parse(html: str):
        #  official_name, url, title, text
        div_boxes = BeautifulSoup(html, "html.parser") \
            .find_all("div", class_="result-op")

        page_info_wrapper = []
        for div_box in div_boxes:
            url = div_box.find("a").attrs["href"]
            title = div_box.find("h3").get_text().strip()
            text = div_box.find("div", class_="c-row").strip()
            official_name = "baidu"

            page_info_wrapper.append((official_name, url, title, text))

        return page_info_wrapper
