from django.urls import path
from .views import RegisterView, LoginView, UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt

app_name = "auth"

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("username_val", csrf_exempt(UsernameValidationView.as_view()), name="username_val"),
    path("email_val", csrf_exempt(EmailValidationView.as_view()), name="email_val"),
    path("login", LoginView.as_view(), name="login"),
]
