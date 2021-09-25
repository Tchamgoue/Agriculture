from django.conf.urls import url
from . import views

urlpatterns = [
    url('list_farmers', views.list_farmers_view, name='list_farmers_view'),
    url('farmer_location', views.farmer_location_view, name='farmer_location_view'),
    url('add_crop_request', views.add_crop_request_view, name='add_crop_request_view'),
    url('list_crop_requests', views.list_crop_requests_view, name='list_crop_requests_view'),
    url('profile', views.profile_view, name='profile_view'),

]
