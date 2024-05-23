from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = "income"

urlpatterns = [
    path("", views.home, name="home"),
    # path("", csrf_exempt(views.home), name="home"),
    path("add", views.add, name="add"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("<int:id>/delete", views.delete, name="delete"),
    path("add_category", views.add_category, name="add_category"),
    path("search", csrf_exempt(views.search), name="search"),
]
