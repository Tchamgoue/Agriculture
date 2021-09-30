from django.conf.urls import url
from . import views


urlpatterns = [
    url('^farm_crops$', views.add_crops_to_farm, name="farm_crops"),
    url('^farm_location$', views.add_farm_location, name="farm_location"),
]