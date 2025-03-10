from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse

from .grasp import getDateInGrasp
from .mysql_connection import sql
import threading

mysql = sql.get_conn()

def search_view(request: HttpRequest):
    words = request.GET.get('words')
    username = request.headers.get("username")

    if username is None:
        return HttpResponseBadRequest("Username是必须的")

    if words is None:
        return HttpResponseBadRequest("请求参数可能有问题，请检查")
    
    cursor = mysql.cursor()
    getDateInGrasp(words)

    cursor.execute("SELECT * FROM website WHERE title LIKE %s", (f"%{words}%", ))
    queryset = [{
        "words": words,
        "title": title,
        "description": description,
        "text": text,
        "fromURL": url,
    } for title, _, url, description, text in cursor.fetchall()]
    
    def add_to_website_tb():
        cursor.execute("SELECT id FROM website WHERE title LIKE %s", (f"%{words}%", ))
        related_title = [ids[0] for ids in cursor.fetchall()]

        cursor.execute("SELECT u_id FROM user WHERE u_name = '%s'" % username)
        (user_id, ) = cursor.fetchone()

        for title_id in related_title:
            cursor.execute("INSERT INTO user_search_website(u_id, website_id) VALUE (%s, %s)" % (user_id, title_id))
            mysql.commit()
    
    threading.Thread(target=add_to_website_tb).start()

    return JsonResponse(queryset, safe=False)



def relate_keyword_view(request: HttpRequest):
    """相关关键字

    Args:
        request (HttpRequest): Http请求对象

    Returns:
        _type_: List[str]
    """
    words = request.GET.get('words')
    if words is None or len(words) == 0:
        return JsonResponse([])
    
    words = words.strip()
    
    cursor = mysql.cursor()
    sql_sentence = "SELECT title FROM website WHERE title LIKE %s OR `text` LIKE %s" % (f"'%{words}%'", f"'%{words}%'")
    cursor.execute(sql_sentence)
    result = cursor.fetchall()

    return JsonResponse([word[0] for word in result], safe=False)
