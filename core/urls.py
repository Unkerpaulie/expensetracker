from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("check/", views.check, name="check"),
    path("month_charts/", csrf_exempt(views.month_charts), name="month_charts"),
    # path("inc_chart/", csrf_exempt(views.inc_chart), name="inc_chart"),
]
