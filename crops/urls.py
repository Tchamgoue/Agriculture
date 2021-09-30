from django.conf.urls import url
from . import views


urlpatterns = [
    url('^crops_registration$', views.crops_registration_view, name="crops_registration"),
]