from django.shortcuts import render


def home(req):
    context = {"current_page": "Home"}
    return render(req, "core/home.html", context)