from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
# from .models import Income, Source
import json


@login_required
def home(req):
    context = {"current_page": "Reports"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}]}
    return render(req, "reports/home.html", context)
