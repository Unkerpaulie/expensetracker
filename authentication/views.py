from django.shortcuts import render
from django.views import View


class RegisterView(View):
    def get(self, req):
        return render(req, "authentication/register.html")

        
class LoginView(View):
    def get(self, req):
        return render(req, "authentication/login.html")

