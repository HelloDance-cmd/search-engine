from typing import List

url = 'https://www.baidu.com/sugrec?pre=1&p=3&ie=utf-8&json=1&prod=pc&from=pc_web&sugsid=61027,62336,62327,62636,62693,62718,62330,62795,62864&csor=1&pwd=a&cb=jQuery1102019854219674500673_1743830260168&_=1743830260170&wd='
import json
import urllib.parse
import requests


def relation_keyword(word):
    url_encode = lambda x: urllib.parse.quote(x)
    encoded_word = url_encode(word)
    temp_url = url + encoded_word
    try:
        response = requests.get(temp_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        json_obj = response.text.replace('jQuery1102019854219674500673_1743830260168', '')
        keyword_details = json.loads(json_obj[1: -1])['g']
        print(keyword_details)
        keywords = list()
        for keyword_detail in keyword_details:
            keywords.append(keyword_detail['q'])

        return keywords
    except Exception as e:
        print(e)
        return list()


def hotpot_word() -> List[str]:
    url = "https://www.baidu.com/"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    html_text = response.text
    print(html_text)
    print(html_text.rfind("总书记心系人民健康"))


hotpot_word()
