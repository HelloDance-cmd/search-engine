
from django.urls import path
from . import views

urlpatterns = [
  path("login/", views.user_login_view),
  path("register/", views.user_register_view)
]