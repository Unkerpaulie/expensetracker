from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from expenses.models import Expense
import json


def home(req):
    context = {"current_page": "Home"}
    return render(req, "core/home.html", context)


def search(req):
    if req.method == "POST":
        search = json.loads(req.body).get("search")
        if search:
            # search through expenses
            expenses = Expense.objects.filter(user=req.user)
            exp_results = expenses.filter(
                Q(amount__icontains=search) | 
                Q(category__icontains=search) | 
                Q(description__icontains=search)
            )
            return JsonResponse(list(exp_results.values()), safe=False)