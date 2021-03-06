from django.shortcuts import render, redirect
from django.http.request import HttpRequest
import odoorpc
import pprint


# Create your views here.

def list_farmers_view(request):
    return render(request, 'admin_farmer/pages/list_farmers.html')


def farmer_location_view(request):
    return render(request, 'admin_farmer/pages/farmer_location.html')

def add_crop_request_view(request):
    return render(request, 'admin_farmer/pages/add_crop_request.html')

def list_crop_requests_view(request):
    return render(request, 'admin_farmer/pages/list_crop_requests.html')

def profile_view(request):
    return render(request, 'admin_farmer/pages/profile.html')