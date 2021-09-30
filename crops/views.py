from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from . import forms


# Create your views here.

def crops_registration_view(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            crop = forms.CropsRegistration(request.POST)
            if crop.is_valid():
                print("ok")
            else:
                print(crop.data)
                return render(request, "crops/crops_registration.html")
        else:
            return render(request, "crops/crops_registration.html")
    else:
        return redirect('home')
