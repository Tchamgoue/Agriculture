from django.conf.urls import url

from . import views

urlpatterns = [
    url('^farmer_registration$', views.farmer_registration_view, name='farmer_registration'),
    url('^farmer_registration_success$', views.farmer_registration_success_view, name='farmer_registration_success'),
    url('^all_farmers$', views.all_farmers_view, name='all_farmers'),
    url('^login$', views.login_view, name='login'),
    url('^contact$', views.contact_view, name='contact'),
    url('^about$', views.about_view, name='about_view'),
    url('^user_account$', views.user_account, name='user_account'),
    url('^logout$', views.logout, name='logout'),
    url('^new_crop_request$', views.new_crop_request, name='new crop request'),
    url('^farmer_crops$', views.farmer_crops, name='Farmer crops'),
    url('^farmer_farms$', views.farmer_farms, name='Farmer farms'),
    url('^farmer_requests$', views.farmer_requests, name='Farmer requests'),
    url('^crops_registration$', views.crops_registration_view, name="crops_registration"),
    url('^farm_location_registration$', views.farm_location_registration_view, name="farm_registration")
]
