from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
import json, re
from django.http import JsonResponse


def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None


class RegisterView(View):
    def get(self, req):
        context = {"page": "register"}
        return render(req, "authentication/register.html", context)

        
class UsernameValidationView(View):
    def post(self, req):
        data = json.loads(req.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse({"username_error": "Username must only contain numbers and letters."}, status=400)
        elif User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "Username already exists. Please choose another."}, status=409)
        return JsonResponse({"username_valid": True})

        
class EmailValidationView(View):
    def post(self, req):
        data = json.loads(req.body)
        email = data["email"]

        if not validate_email(email):
            return JsonResponse({"email_error": "Please enter a valid email address."}, status=400)
        elif User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "This email already exists. Please choose another."}, status=409)
        return JsonResponse({"email_valid": True})

        
class LoginView(View):
    def get(self, req):
        context = {"page": "login"}
        return render(req, "authentication/login.html", context)

