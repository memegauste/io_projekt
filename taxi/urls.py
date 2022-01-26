"""Taxi urls file."""
from django.urls import path
from taxi.views import RobotsView
from taxi.views import IndexView

app_name = 'taxi'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('robots.txt', RobotsView.as_view(), name='robots'),
]
