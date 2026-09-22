from django.urls import path
from .views import login
from django.contrib.auth import views

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
