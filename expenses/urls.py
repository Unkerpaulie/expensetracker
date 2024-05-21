from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path("", views.home, name="home"),
    path("add", views.add, name="add"),
    path("add_category", views.add_category, name="add_category"),
]
