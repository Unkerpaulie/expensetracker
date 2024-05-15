from django.shortcuts import render
from django.views import View


class RegisterView(View):
    def get(self, req):
        context = {"page": "register"}
        return render(req, "authentication/register.html", context)

        
class LoginView(View):
    def get(self, req):
        context = {"page": "login"}
        return render(req, "authentication/login.html", context)

