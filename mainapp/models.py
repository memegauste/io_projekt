"""Mainapp models file."""
from django.db import models


class Klient(models.Model):
    """Model klienta."""

    idKlienta = models.IntegerField(primary_key=True)
    imieKlienta = models.CharField(max_length=50)
    nrTelefonu = models.CharField(max_length=9)
    dlugoscGeoKlienta = models.FloatField()
    szerokoscGeoKlienta = models.FloatField()

    def __str__(self):
        return f'{self.imieKlienta}'


class Dyspozytor(models.Model):
    """Model dyspozytora."""

    idDyspozytra = models.IntegerField(primary_key=True)
    imieDyspozytora = models.CharField(max_length=50)
    nazwiskoDyspozytora = models.CharField(max_length=50)

    def __str__(self):  # noqa: D106
        return f'{self.imieDyspozytora} {self.nazwiskoDyspozytora}'


class Kierowca(models.Model):
    """Model kierowcy."""

    idKierowcy = models.IntegerField(primary_key=True)
    imieKierowcy = models.CharField(max_length=50)
    nazwiskoKierowcy = models.CharField(max_length=50)
    dlugoscGeoKierowcy = models.FloatField()
    szerokoscGeoKierowcy = models.FloatField()

    def __str__(self):  # noqa: D106
        return f'{self.imieKierowcy} {self.nazwiskoKierowcy}'


class Usluga(models.Model):

    idUsluga = models.IntegerField(primary_key=True)
    idDyspozytora = models.IntegerField()
    idKierowcy = models.ForeignKey(Kierowca, on_delete=models.CASCADE)
    idKlienta = models.ForeignKey(Klient, on_delete=models.CASCADE)
    dlugoscGeoCelu = models.FloatField()
    szerokoscGeoCelu = models.FloatField()

    def __str__(self):  # noqa: D106
        return f'Usługa o id {self.idUsluga}'