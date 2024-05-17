from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages, auth
import json, re
from django.http import JsonResponse
from django.core.mail import EmailMessage


def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def send_activation_email(user):
    body = """
Please follow the link provide to activate your account.
"""
    email = EmailMessage(
        subject="Activate you Expense Tracke account",
        body=body,
        from_email="noreply@localhost.run",
        to=user.email,
    )

class RegisterView(View):
    def get(self, req):
        context = {"page": "register"}
        return render(req, "authentication/register.html", context)

    def post(self, req):
        # info already valid
        data = req.POST
        username = data["username"]
        email = data["email"]
        password = data["password"]

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        # set up cnfirmation email to activate accout

        if user.id:
            messages.success(req, "Registration successful! You may now log in")
            return redirect("auth:login")

        # if an error occured, return user to form with values restored
        messages.warning(req, "Registration failed! Please try again")
        context = {"page": "register", "fieldvalues": data}
        return render(req, "authentication/register.html", context)

        
class UsernameValidationView(View):
    def post(self, req):
        data = json.loads(req.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse({"username_error": "Username must only contain numbers and letters."})
        elif User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "Username already exists. Please choose another."})
        return JsonResponse({"username_valid": True})

        
class EmailValidationView(View):
    def post(self, req):
        data = json.loads(req.body)
        email = data["email"]

        if not validate_email(email):
            return JsonResponse({"email_error": "Please enter a valid email address."})
        elif User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "This email already exists. Please choose another."})
        return JsonResponse({"email_valid": True})

        
class LoginView(View):
    def get(self, req):
        context = {"page": "login"}
        return render(req, "authentication/login.html", context)

    def post(self, req):
        # info already valid
        data = req.POST
        username = data["username"]
        password = data["password"]

        user = auth.authenticate(username=username, password=password)
        # set up cnfirmation email to activate accout

        if user:
            auth.login(req, user)
            messages.success(req, f"Welcome, {user.username}!")
            return redirect("core:home")

        # if an error occured, return user to form with values restored
        messages.warning(req, "Incorrect credentials. Please try again.")
        context = {"page": "login", "fieldvalues": data}
        return render(req, "authentication/login.html", context)


class LogoutView(View):
    def get(self, req):
        auth.logout(req)
        return redirect("core:home")
