import time
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.db.models import Q

from search.models import Website, User

from .grasp import getDateInGrasp
import threading

def search_view(request: HttpRequest):
    words = request.GET.get('words')
    username = request.headers.get("username")
    if username is None:
        return HttpResponseBadRequest("Username是必须的")

    if words is None:
        return HttpResponseBadRequest("请求参数可能有问题，请检查")
    
    getDateInGrasp(words)
    # threading.Thread(target=getDateInGrasp, args=(words,))
    # 在3s内能爬取多少算多少
    # duration = 10
    # time.sleep(duration)

    match_title_results = Website.objects.filter(title__icontains=words).all()
    queryset = [{
        "words": words,
        "title": match_title.title,
        "description": match_title.description,
        "text": match_title.content,
        "fromURL": match_title.address,
        "category": match_title.categories.name
    } for match_title in match_title_results]
    
    def add_to_website_tb():
        match_ids = Website.objects.filter(title__icontains=words).values_list('id', flat=True)
        website_ids = [id for id in match_ids]
        user_id = User.objects.filter(name=username).first()

        if user_id is None:
            return
        
        unamed_user = User(pk=user_id)
        for website_id in website_ids:
            website = Website.objects.filter(pk=website_id).first()
            
            if website is None:
                continue

            unamed_user.visited_website.add(website)
        # unamed_user.save()


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
    all_words = Website.objects.filter(Q(title__icontains=words) | Q(text__icontains=words)).values_list('title')

    return JsonResponse([word for word in all_words], safe=False)
