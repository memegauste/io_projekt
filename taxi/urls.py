"""Taxi urls file."""
from django.urls import path
from taxi.views import RobotsView, load_drivers
from taxi.views import IndexView

app_name = 'taxi'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pobierz-kierowcow/', load_drivers, name='load_drivers'),
    path('robots.txt', RobotsView.as_view(), name='robots'),
]
