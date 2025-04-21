from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login_view),
    path("register/", views.user_register_view),
    path("userProfile/", views.get_user_profile),
    path('changeUserName/', views.user_change_username),
    path('changePassword/', views.user_change_password)
]
