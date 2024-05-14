from django.shortcuts import render


def home(req):
    return render(req, "expenses/home.html")