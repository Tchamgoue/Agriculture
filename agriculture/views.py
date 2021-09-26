from django.shortcuts import render
from django.http.request import HttpRequest


def home(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            pass
        else:
            return render(request, 'index.html')
    else:
        print("not a request from navigator !")
