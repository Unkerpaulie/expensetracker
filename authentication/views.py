from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


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

        
class LoginView(View):
    def get(self, req):
        context = {"page": "login"}
        return render(req, "authentication/login.html", context)

