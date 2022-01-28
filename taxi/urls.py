"""Taxi urls file."""
from django.urls import path
from taxi.views import load_drivers
from taxi.views import load_available_drivers
from taxi.views import RobotsView
from taxi.views import DyspozytorView

app_name = 'taxi'

urlpatterns = [
    path('panel-dyspozytora/<int:pk>/', DyspozytorView.as_view(), name='index'),
    path('panel-dyspozytora/', DyspozytorView.as_view(), name='index'),
    path('pobierz-kierowcow/', load_drivers, name='load_drivers'),
    path('pobierz-dostepnych-kierowcow/', load_available_drivers, name='load_available_drivers'),
    path('robots.txt', RobotsView.as_view(), name='robots'),
]
