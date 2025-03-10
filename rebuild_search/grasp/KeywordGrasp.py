from typing import List, Tuple
from urllib.parse import quote
from bs4 import BeautifulSoup

from .Graps import Grasp
from rebuild_search.mysql_connection import sql

mysql = sql.get_conn()

class GraspByKeyword(Grasp):
    def __init__(self, word: str):
        super().__init__()

        self.urls = {
            "sina": lambda k: f"https://search.sina.com.cn/?q={quote(k)}&c=news&from=channel&ie=utf-8",
            "cctv": lambda k, page=1: f"https://search.cctv.com/search.php?qtext={quote(k)}&type=web&page={page}",
            "baidu": lambda k, page=1: f"https://www.baidu.com/s?tn=news&ie=utf-8&word={quote(k)}&pn={(page - 1) * 10}"
        }

        self.word = word

    def start(self):
        self.grasp_by_keyword(self.word)

    def grasp_by_keyword(self, k, page = 10):
        page = 10 if page is None else page

        sina_once = True
        for cur_page in range(1, page + 1):  # 爬取10页数据
            for official_name in self.urls:
                # 过滤掉新浪
                # 新浪不可以进行分页查找
                if official_name == "sina":
                    self.url = self.urls[official_name](k)
                else:
                    self.url = self.urls[official_name](k, cur_page)

                text = self.grasp()
                page_info_wrapper = []

                if sina_once and official_name.find("sina") != -1:
                    sina_once = False  # 只进行一次sina的查询
                    page_info_wrapper = GraspByKeyword.sina_parse(text)
                elif official_name.find("cctv") != -1:
                    page_info_wrapper = GraspByKeyword.cctv_parse(text)
                elif official_name.find("baidu") != -1:
                    page_info_wrapper = GraspByKeyword.baidu_parse(text)

                if page_info_wrapper:
                    GraspByKeyword.add_to_mysql(page_info_wrapper, k)

    @staticmethod
    def add_to_mysql(page_info_wrapper: List[Tuple[str, str, str, str]], k):
        if not page_info_wrapper:
            return

        cursor = mysql.cursor()
        
        for _, url, title, text in page_info_wrapper:
            sql_sentence = "INSERT INTO `website`(`title`, `url`, `description`, `text`) VALUES ('%s', '%s', '%s', '%s')" % (title, url, text[: 50], text)
            cursor.execute(sql_sentence)
            mysql.commit()
        cursor.close()

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
