import json
import urllib.parse
from asyncio import timeout

import requests
import urllib3.util
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.db.models import Q

from modules.models import Website, User

from .grasp import getDateInGrasp
import threading


def search_view(request: HttpRequest):
    words = request.GET.get('words')
    username = request.headers.get("username")

    if username is None:
        return HttpResponseBadRequest("Username是必须的")

    if words is None:
        return HttpResponseBadRequest("请求参数可能有问题，请检查")

    user = User.objects.get(name=username)
    if user is None:
        return HttpResponseBadRequest(f"{username} 没有注册")

    # 爬取新聞數據
    getDateInGrasp(words, user.id)

    match_title_results = Website.objects.filter(title__icontains=words).all()
    queryset = [{
        "words": words,
        "title": match_title.title,
        "description": match_title.description,
        "text": match_title.content,
        "fromURL": match_title.address,
        "category": match_title.categories.name
    } for match_title in match_title_results]

    def user_visited_website():
        match_ids = Website.objects.filter(title__icontains=words).values_list('id', flat=True)
        website_ids = [id for id in match_ids]
        user_id = User.objects.filter(name=username).first()

        if user_id is None:
            return

        # 用戶訪問過此網站
        # 添加網站和用戶的
        unamed_user = User(pk=user_id)
        for website_id in website_ids:
            website = Website.objects.filter(pk=website_id).first()

            if website is None:
                continue

            unamed_user.visited_website.add(website)

    # 這個不重要，可以不需要占用整個請求流程
    # 添加用戶和網站的關聯
    threading.Thread(target=user_visited_website).start()
    return JsonResponse(queryset, safe=False)


url = 'https://www.baidu.com/sugrec?pre=1&p=3&ie=utf-8&json=1&prod=pc&from=pc_web&sugsid=61027,62336,62327,62636,62693,62718,62330,62795,62864&csor=1&pwd=a&cb=jQuery1102019854219674500673_1743830260168&_=1743830260170&wd='

def relate_keyword_view(request: HttpRequest):
    if request.method != 'GET':
        return JsonResponse(["请求格式有误"], safe=False)
    words = request.GET.get('words')
    if words is None or len(words) == 0:
        return JsonResponse([], safe=False)

    url_encode = lambda x: urllib.parse.quote(x)
    encoded_word = url_encode(words)
    temp_url = url + encoded_word
    try:
        response = requests.get(temp_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        json_obj = response.text.replace('jQuery1102019854219674500673_1743830260168', '')
        json_obj = json.loads(json_obj[1: -1])
        return JsonResponse(json_obj, safe=False)
    except Exception as e:
        return JsonResponse([e], safe=False)