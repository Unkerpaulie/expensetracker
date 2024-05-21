from django.shortcuts import render, redirect
from .models import Expense, Category
from django.contrib import messages


def home(req):
    context = {"current_page": "Expenses"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}]}
    return render(req, "expenses/home.html", context)


def add(req):
    categories = Category.objects.all()
    context = {"current_page": "Add Expense"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}, {"label": "Expenses", "url": "expenses:home"}]}
    context["categories"] = categories
    if req.method == "POST":
        # flush messages
        valid = True
        form_data = req.POST
        print(req.POST)
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
            messages.success(req, "Expense added")
            Expense.objects.create(user=req.user, amount=amount, category=Category.objects.get(name=category), description=description, expense_date=expense_date)
            return redirect("expenses:home")

    return render(req, "expenses/add.html", context)


def add_category(req):
    # does not render template
    if req.method == "POST":
        if req.POST["cat"]:
            Category.objects.create(name=req.POST["cat"])
        return redirect("expenses:add")
    
