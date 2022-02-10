
from django.urls import path

from . import views

urlpatterns = [
    path('farmer_registration', views.farmer_registration_view, name='farmer_registration'),
    path('farmer_registration_success', views.farmer_registration_success_view, name='farmer_registration_success'),
    path('all_farmers', views.all_farmers_view, name='all_farmers'),
    path('login', views.login_view, name='login'),
    path('contact', views.contact_view, name='contact'),
    path('about', views.about_view, name='about_view'),
    path('user_account', views.user_account, name='user_account'),
    path('logout', views.logout, name='logout'),
    path('new_crop_request', views.new_crop_request, name='new crop request'),
    path('farmer_crops', views.farmer_crops, name='Farmer crops'),
    path('farmer_farms', views.farmer_farms, name='Farmer farms'),
    path('farmer_requests', views.farmer_requests, name='Farmer requests'),
    path('crops_registration', views.crops_registration_view, name="crops_registration"),
    path('farm_location_registration', views.farm_location_registration_view, name="farm_registration"),
    path("agro-similarity",views.agro_similarity_view,name="agroviews"),
    path("demo-agro-similarity",views.perfom_demo,name="demoagro")
]
