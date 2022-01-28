"""Admin file."""

# Register your models here.
from django.contrib import admin
from taxi.models import Dyspozytor
from taxi.models import Kierowca
from taxi.models import Klient
from taxi.models import Usluga


@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):  # noqa: D101

    list_display = [
        'idKlienta',
        'imieKlienta',
        'nrTelefonu',
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
