from django.shortcuts import render
from django.http.request import HttpRequest


def home(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            pass
        else:
            return render(request, 'index.html', {
                'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                'username': request.session['username'] if 'username' in request.session.keys() else None,
            })
    else:
        print("not a request from navigator !")
