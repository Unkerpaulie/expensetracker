from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from pathlib import Path
from .models import Preference

@login_required(redirect_field_name=None)
def home(req):
    context = {"current_page": "Settings"}
    context |= {"backlinks": [{"label": "Home", "url": "core:home"}]}
    # check if preference already exists
    if req.method == "POST":
        pref = Preference.objects.filter(user=req.user).first()
        if req.POST.get("curr"):
            if pref:
                pref.currency = req.POST.get("curr")
                pref.save()
            else:
                Preference.objects.create(user=req.user, currency=req.POST.get("curr"))
            messages.success(req, "Currency updated.")
        else:
            messages.warning(req, "Please choose a currency from the list")

    file_path = settings.BASE_DIR / "currencies.json"
    # debugging for python
    # import pdb
    # pdb.set_trace()
    with open(file_path, "r") as f:
        data = json.load(f)

    currencies = [{"abbr": k, "name": v} for k, v in data.items()]
    pref = Preference.objects.filter(user=req.user).first()
    context |= {"currencies": currencies, "pref": pref}
    return render(req, "preference/home.html", context)