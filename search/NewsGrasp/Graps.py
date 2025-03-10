"""
    抓取工具
    1. 爬取网页内容
    2. 管理requests的一些配置项
"""
import requests


class Grasp:
    def __init__(self, url: str = ""):
        self.url = url

    def grasp(self):
        if self.url == "":
            raise Exception("URL must be exists")

        response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        response.encoding = response.apparent_encoding
        response.raise_for_status()

        return response.text
