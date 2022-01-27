"""Taxi urls file."""
from django.urls import path
from mobile.views import ClientMobileView

app_name = 'mobile'

urlpatterns = [
    path('', ClientMobileView.as_view(), name='index'),
]