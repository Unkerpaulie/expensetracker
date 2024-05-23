from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Income, IncomeCategory
import json


@login_required
def home(req):
    context = {"current_page": "Income"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}]}
    context["namespace"] = "income"
    currency = req.user.preference.currency
    context["currency"] = currency
    income = Income.objects.filter(user=req.user)
    paginator = Paginator(income, 5)
    page_num = req.GET.get("page", 1)
    page_data= paginator.get_page(page_num)
    context["page_data"] = page_data
    return render(req, "expenses/home.html", context)


def search(req):
    if req.method == "POST":
        search = json.loads(req.body).get("search")
        if search:
            # search through income
            income = Income.objects.filter(user=req.user)
            exp_results = income.filter(
                Q(amount__icontains=search) | 
                Q(category__name__icontains=search) | 
                Q(description__icontains=search) 
            )
            return JsonResponse(list(exp_results.values()), safe=False)


@login_required
def add(req):
    categories = IncomeCategory.objects.all()
    context = {"current_page": "Add Income"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}, {"label": "Income", "url": "income:home"}]}
    context["categories"] = categories
    if req.method == "POST":
        valid = True
        form_data = req.POST
        amount = form_data["amount"]
        category = form_data["category"]
        description = form_data["description"]
        expense_date = form_data["expense_date"]
        if not amount:
            valid = False
            messages.warning(req, "You must enter a numeric amount")
        if not expense_date:
            valid = False
            messages.warning(req, "Please enter a valid date")
        if not valid:
            context |= {"form_data": form_data}
            return render(req, "expenses/add.html", context)
        else:
            messages.success(req, "Income added")
            Income.objects.create(user=req.user, amount=amount, category=IncomeCategory.objects.get(name=category), description=description, expense_date=expense_date)
            return redirect("income:home")

    return render(req, "expenses/add.html", context)


@login_required
def add_category(req):
    # does not render template
    if req.method == "POST":
        new_cat = req.POST["cat"]
        cat_list = IncomeCategory.objects.values_list("name", flat=True)
        # print(cat_list)
        if new_cat:
            if new_cat in cat_list:
                messages.warning(req, f"The category {new_cat} already exists")
            else:
                IncomeCategory.objects.create(name=new_cat)
                messages.success(req, f"{new_cat} added to Categories")
        else:
            messages.warning(req, f"No new category was added")
        return redirect("income:add")
   
    
@login_required
def edit(req, id):
    categories = IncomeCategory.objects.all()
    expense = Income.objects.get(pk=id)

    context = {"current_page": "Edit Income"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}, {"label": "Income", "url": "income:home"}]}
    context["categories"] = categories
    context["form_data"] = {
        "category": expense.category.name,
        "description": expense.description,
        "amount": expense.amount,
        "expense_date": expense.expense_date.strftime("%Y-%m-%d")
    }

    if req.method == "POST":
        # flush messages
        valid = True
        form_data = req.POST
        amount = form_data["amount"]
        category = form_data["category"]
        description = form_data["description"]
        expense_date = form_data["expense_date"]
        if not amount:
            valid = False
            messages.warning(req, "You must enter a numeric amount")
        if not expense_date:
            valid = False
            messages.warning(req, "Please enter a valid date")
        if not valid:
            context |= {"form_data": form_data}
            return render(req, "expenses/add.html", context)
        else:
            expense.amount = amount
            expense.category = IncomeCategory.objects.get(name=category)
            expense.description = description
            expense.expense_date = expense_date
            expense.save()
            messages.success(req, "Income updated")
            return redirect("income:home")

    return render(req, "expenses/add.html", context)


@login_required
def delete(req, id):
    if req.method == "POST":
        expense = Income.objects.get(pk=id)
        expense.delete()
        messages.info(req, f"Income {expense} was deleted")
        return redirect("income:home")


