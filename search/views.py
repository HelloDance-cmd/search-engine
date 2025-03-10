# Create your views here.
import datetime
from typing import List, override
from django.views import View
from django.http import HttpResponse, JsonResponse

from search.NewsGrasp import KeywordGrasp
from search.mysql_connection.sql_wrench import mysql
from search.utils import sqls
from search.utils.config import MAX_CNT
from threading import Thread


class SearchView(View):
    def get(self, request, *args, **kwargs):
        words = self.request.GET.get('words')

        if words is None:
            return HttpResponse("请求参数可能有问题，请检查")

        ret = []

        cursor = mysql.cursor()
        # 如果没有这个关键词
        # 就需要启动Python爬虫工具进行相应爬取
        count: int = cursor.execute("SELECT id FROM words WHERE words = %s", (words,))
        if count == 0:
            Thread(None, KeywordGrasp.GraspByKeyword(words).start).start()
            # KeywordGrasp.GraspByKeyword(words) \
            #     .start()
        queryset = ()

        while len(queryset) == 0:
            cursor.execute(
                sqls.select_details_of_word(words))
            queryset = cursor.fetchall()
        
        cursor.execute(
            sqls.select_relate_tags())
        
        relate_tags = cursor.fetchall()

        def get_tag(w: str) -> List[str]:
            ans = []
            for tag in relate_tags:
                if tag[1] == w:
                    ans.append(tag[0])
            return ans

        for words, title, text, url in queryset:
            ret.append({
                "words": words,
                "title": title,
                "content": text,
                "fromURL": url,
                "tags": get_tag(words),
                "created_at": str(datetime.datetime.now())
            })
        cursor.close()
        return JsonResponse(ret, safe=False)



class RelateKeywordsView(View):
    """
        当用于键入的时候提示相关关键字
    """

    @override
    def get(self, reqeust, *args, **kwargs):
        words = self.request.GET.get('words')

        if words is None or len(words) == 0:
            return JsonResponse([])
      
        cursor = mysql.cursor()

        cursor.execute(sqls.select_relate_words(words))
        cursor.close()

        return JsonResponse([word[0] for word in cursor.fetchmany(MAX_CNT)], safe=False)


class SearchTagsView(View):
    @override
    def get(self, *args, **kwargs):
        cursor = mysql.cursor()

        cursor.execute("SELECT tag_name FROM tag")
        cursor.close()
        
        return JsonResponse([tag[0] for tag in cursor.fetchmany(MAX_CNT)], safe=False)
