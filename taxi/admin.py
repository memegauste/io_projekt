"""Admin file."""

# Register your models here.
from django.contrib import admin

from taxi.models import Dyspozytor, Kierowca, Klient, Usluga


@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):  # noqa: D101

    list_display = [
        'idKlienta',
        'imieKlienta',
        'nrTelefonu',
        'dlugoscGeoKlienta',
        'szerokoscGeoKlienta',
    ]


@admin.register(Dyspozytor)
class DyspozytorAdmin(admin.ModelAdmin):  # noqa: D101

    list_display = [
        'idDyspozytora',
        'imieDyspozytora',
        'nazwiskoDyspozytora',
    ]


@admin.register(Kierowca)
class KierowcaAdmin(admin.ModelAdmin):  # noqa: D101

    list_display = [
        'idKierowcy',
        'imieKierowcy',
        'nazwiskoKierowcy',
        'dlugoscGeoKierowcy',
        'szerokoscGeoKierowcy',
    ]


@admin.register(Usluga)
class UslugaAdmin(admin.ModelAdmin):  # noqa: D101

    list_display = [
        'idUsluga',
        'idDyspozytora',
        'idKierowcy',
        'idKlienta',
        'dlugoscGeoCelu',
        'szerokoscGeoCelu',
    ]
