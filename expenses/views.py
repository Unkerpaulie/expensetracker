from django.shortcuts import render


def home(req):
    context = {"current_page": "Expenses"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}]}
    return render(req, "expenses/home.html", context)


def add(req):
    context = {"current_page": "Add Expense"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}, {"label": "Expenses", "url": "expenses:home"}]}
    return render(req, "expenses/add.html", context)

