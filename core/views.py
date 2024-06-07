from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from expenses.models import Expense, Category
from income.models import Income, Source
import json, calendar
import pandas as pd


# utility functions
def expense_data(u):
    exp = pd.DataFrame(list(Expense.objects.filter(user=u).values()))
    if not exp.empty:
        cat = pd.DataFrame(list(Category.objects.all().values()))
        exp["expense_date"] = pd.to_datetime(exp['expense_date'])
        exp_data = exp.merge(cat, left_on="category_id", right_on="id", suffixes=('', '_y'))
        exp_data = exp_data.drop('id_y', axis=1)
        exp_data["month"] = exp_data["expense_date"].dt.month
        exp_data["year"] = exp_data["expense_date"].dt.year
        return exp_data
    return exp


def income_data(u):
    inc = pd.DataFrame(list(Income.objects.filter(user=u).values()))
    if not inc.empty:
        src = pd.DataFrame(list(Source.objects.all().values()))
        inc["income_date"] = pd.to_datetime(inc['income_date'])
        inc_data = inc.merge(src, left_on="source_id", right_on="id", suffixes=('', '_y'))
        inc_data = inc_data.drop('id_y', axis=1)
        inc_data["month"] = inc_data["income_date"].dt.month
        inc_data["year"] = inc_data["income_date"].dt.year
        return inc_data
    return inc
    

# route functions
def home(req):
    context = {"current_page": "Home"}
    if req.user.is_authenticated:
        # get months for chart filtering
        exp = expense_data(req.user)
        inc = income_data(req.user)
        if not exp.empty or not inc.empty:
            months = list(set([m for m in exp["month"]] + [m for m in inc["month"]]))
            months.sort()
            month_select = [{"num": m, "month_name": calendar.month_name[m]} for m in months]
            context |= {"months": month_select}
        else:
            context |= {"nodata": True}
    return render(req, "core/home.html", context)


def month_charts(req):
    context = {}

    exp = expense_data(req.user)
    inc = income_data(req.user)
    if not exp.empty:
        exp = exp[exp["user_id"] == req.user.id]
        if req.method == "POST" and int(req.POST.get("month", 0)[0]) != 0:
            # filter if month
            m = int(req.POST.get("month", 0)[0])
            exp = exp[exp["month"] == m]
        exp = exp[["name", "amount"]]
        exp = exp.groupby(["name"]).sum().sort_values(by="amount", ascending=False)
        exp_chart = {}
        exp_chart["labels"] = exp.index.tolist()
        exp_chart["values"] = exp["amount"].tolist()
        exp_chart["total"] = exp["amount"].sum()
        exp_chart["currency"] = req.user.preference.currency
        context["exp_chart"] = exp_chart
    else:
        context["exp_chart"] = False

    if not inc.empty:
        inc = inc[inc["user_id"] == req.user.id]
        if req.method == "POST" and int(req.POST.get("month", 0)[0]) != 0:
            # filter if month
            m = int(req.POST.get("month", 0)[0])
            inc = inc[inc["month"] == m]
        inc = inc[["name", "amount"]]
        inc = inc.groupby(["name"]).sum().sort_values(by="amount", ascending=False)
        inc_chart = {}
        inc_chart["labels"] = inc.index.tolist()
        inc_chart["values"] = inc["amount"].tolist()
        inc_chart["total"] = inc["amount"].sum()
        inc_chart["currency"] = req.user.preference.currency
        context["inc_chart"] = inc_chart
    else:
        context["inc_chart"] = False

    return JsonResponse(context)


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
        
def maybe(req):
    res = f"<p>{req.user}</p>"
    res += f"<p>{req.user.is_authenticated}</p>"
    return HttpResponse(res)


def check(req):
    res = f"<h3>{Source.objects.model._meta.db_table}</h3>"
    res += "<ul>"
    res += "".join([f"<li>{f.name}</li>" for f in Source._meta.get_fields()])
    res += "</ul>"
    res += f"<h3>Expenses</h3>"
    res += "<ul>"
    res += "".join([f"<li>{f.name}: {f.expenses.count()}</li>" for f in Category.objects.all()])
    res += "</ul>"
    res += f"<h3>Expenses{req.user.preference.currency}</h3>"
    res += expense_data(req.user).to_html()
    res += income_data(req.user).to_html()
    inc = income_data(req.user)
    inc= inc[inc["month"] == 5]
    res += inc.to_html()
    return HttpResponse(res)