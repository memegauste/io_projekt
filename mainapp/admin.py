"""Admin file."""

# Register your models here.
from django.contrib import admin

from mainapp.models import Klient, Dyspozytor, Kierowca, Usluga


@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):

    list_display = [
        '__all__',
    ]


@admin.register(Dyspozytor)
class DyspozytorAdmin(admin.ModelAdmin):

    list_display = [
        '__all__',
    ]


@admin.register(Kierowca)
class KierowcaAdmin(admin.ModelAdmin):

    list_display = [
        '__all__',
    ]


@admin.register(Usluga)
class UslugaAdmin(admin.ModelAdmin):

    list_display = [
        '__all__',
    ]
