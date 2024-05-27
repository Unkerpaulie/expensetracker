from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from expenses.models import Expense, Category
from income.models import Income, Source
import json, calendar
import pandas as pd


# utility functions
def expense_data():
    exp = pd.DataFrame(list(Expense.objects.all().values()))
    cat = pd.DataFrame(list(Category.objects.all().values()))
    exp["expense_date"] = pd.to_datetime(exp['expense_date'])
    exp_data = exp.merge(cat, left_on="category_id", right_on="id", suffixes=('', '_y'))
    exp_data = exp_data.drop('id_y', axis=1)
    exp_data["month"] = exp_data["expense_date"].dt.month
    exp_data["year"] = exp_data["expense_date"].dt.year
    return exp_data
    
def income_data():
    inc = pd.DataFrame(list(Income.objects.all().values()))
    src = pd.DataFrame(list(Source.objects.all().values()))
    inc["income_date"] = pd.to_datetime(inc['income_date'])
    inc_data = inc.merge(src, left_on="source_id", right_on="id", suffixes=('', '_y'))
    inc_data = inc_data.drop('id_y', axis=1)
    inc_data["month"] = inc_data["income_date"].dt.month
    inc_data["year"] = inc_data["income_date"].dt.year
    return inc_data
    

# route functions
def home(req):
    context = {"current_page": "Home"}
    # get months for chart filtering
    exp = expense_data()
    inc = income_data()
    months = list(set([m for m in exp["month"]] + [m for m in inc["month"]]))
    months.sort()
    month_select = [{"num": m, "month_name": calendar.month_name[m]} for m in months]
    context |= {"months": month_select}
    return render(req, "core/home.html", context)


def month_charts(req):
    context = {}
    exp = expense_data()
    exp = exp[exp["user_id"] == req.user.id]
    inc = income_data()
    inc = inc[inc["user_id"] == req.user.id]
    print("posty:", req.POST)

    if req.method == "POST" and int(req.POST.get("month", 0)[0]) != 0:
        # filter if month
        m = int(req.POST.get("month", 0)[0])
        print("m", m)
        exp = exp[exp["month"] == m]
        inc = inc[inc["month"] == m]

    # get data for charts 
    exp = exp[["name", "amount"]]
    exp = exp.groupby(["name"]).sum().sort_values(by="amount", ascending=False)
    exp_chart = {}
    exp_chart["labels"] = exp.index.tolist()
    exp_chart["values"] = exp["amount"].tolist()
    exp_chart["total"] = exp["amount"].sum()
    exp_chart["currency"] = req.user.preference.currency

    inc = inc[["name", "amount"]]
    inc = inc.groupby(["name"]).sum().sort_values(by="amount", ascending=False)
    inc_chart = {}
    inc_chart["labels"] = inc.index.tolist()
    inc_chart["values"] = inc["amount"].tolist()
    inc_chart["total"] = inc["amount"].sum()
    inc_chart["currency"] = req.user.preference.currency

    context["exp_chart"] = exp_chart
    context["inc_chart"] = inc_chart


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
    res += expense_data().to_html()
    res += income_data().to_html()
    inc = income_data()
    inc= inc[inc["month"] == 5]
    res += inc.to_html()
    return HttpResponse(res)