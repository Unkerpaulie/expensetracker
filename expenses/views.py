from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Expense, Category


def home(req):
    context = {"current_page": "Expenses"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}]}
    expenses = Expense.objects.filter(user=req.user)
    context["expenses"] = expenses
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
        new_cat = req.POST["cat"]
        cat_list = Category.objects.values_list("name", flat=True)
        # print(cat_list)
        if new_cat:
            if new_cat in cat_list:
                messages.warning(req, f"The category {new_cat} already exists")
            else:
                Category.objects.create(name=new_cat)
                messages.success(req, f"{new_cat} added to Categories")
        else:
            messages.warning(req, f"No new category was added")
        return redirect("expenses:add")
    
def edit(req, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)

    context = {"current_page": "Edit Expense"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}, {"label": "Expenses", "url": "expenses:home"}]}
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
            expense.category = Category.objects.get(name=category)
            expense.description = description
            expense.expense_date = expense_date
            expense.save()
            messages.success(req, "Expense updated")
            return redirect("expenses:home")

    return render(req, "expenses/add.html", context)
