from django.urls import path
from . import views

urlpatterns = [
    path("search_word_contents/", views.SearchView.as_view()),
    path("relate_keywords/", views.RelateKeywordsView.as_view()),
    path("search_tags/", views.SearchTagsView.as_view()),
]