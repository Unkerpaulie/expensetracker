from django.urls import path
from . import views

app_name = "preference"

urlpatterns = [
    path("", views.home, name="home"),
]
