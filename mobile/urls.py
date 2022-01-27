"""Taxi urls file."""
from django.urls import path
from mobile.views import ClientMobileView, add_driver_to_state
from mobile.views import SearchForDriverView

app_name = 'mobile'

urlpatterns = [
    path('<int:driver>/', ClientMobileView.as_view(), name='index'),
    path('', ClientMobileView.as_view(), name='index'),
    path('kierowca-online/', add_driver_to_state, name='add_to_state'),
]