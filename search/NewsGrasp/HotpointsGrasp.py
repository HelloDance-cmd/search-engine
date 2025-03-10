"""
    新闻爬取工具
"""
from typing import List, Tuple

from bs4 import BeautifulSoup
from search.NewsGrasp.Graps import Grasp
from search.NewsGrasp.settings import URLS
from search.mysql_connection.sql_wrench import mysql

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

        cursor = mysql.cursor()
        values = ""
        for official_name, url, _ in url_and_title:
            affect_rows = cursor.execute("SELECT id FROM url WHERE url = %s", (url,))

            if affect_rows != 0:
                continue

            values += "('" + official_name + "','" + url + "', NULL),"

        # 去除已经添加进去的
        if values == "":
            return

        # 填入URL表
        cursor.execute(f"INSERT INTO url(official_name, url, words_id) VALUES {values[: -1]}")
        mysql.commit()

        # 填入到text表
        for official_name, url, title in url_and_title:
            affect_rows = cursor.execute("SELECT id FROM text WHERE title=%s", title)
            if affect_rows != 0:
                continue

            cursor.execute("SELECT id FROM url WHERE url=%s", url)
            url_id = cursor.fetchone()[0]  # 可能空指针异常
            cursor.execute(f"INSERT INTO text(url_id, words_id, title) VALUE ({url_id}, NULL, '{title}')")
            mysql.commit()
        cursor.close()

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
