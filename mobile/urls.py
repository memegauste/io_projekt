"""Taxi urls file."""
from django.urls import path
from mobile.views import ClientMobileView
from mobile.views import SearchForDriverView

app_name = 'mobile'

urlpatterns = [
    path('', ClientMobileView.as_view(), name='index'),
    path('search-driver/', SearchForDriverView.as_view(), name='search_driver'),
]