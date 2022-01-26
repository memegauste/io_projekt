"""Project urls."""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
]
