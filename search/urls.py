from django.urls import path
from . import views


urlpatterns = [
    path("search_word_contents/", views.search_view),
    path("relate_keywords/", views.relate_keyword_view),
    path('hotpots_view/', views.hotpots_view)
]