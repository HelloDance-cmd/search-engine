
from django.urls import path
from . import views

urlpatterns = [
  path("login/", views.userLoginView),
  path("register/", views.userRegisterView)
]