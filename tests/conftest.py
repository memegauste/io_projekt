"""Shared fixtures for the taxi application."""
import pytest

from mobile.utils import state_dict
from taxi.models import Dyspozytor, Kierowca, Klient, Usluga


@pytest.fixture(autouse=True)
def isolated_driver_state():
    state_dict.clear()
    yield
    state_dict.clear()


@pytest.fixture
def dispatcher(db):
    return Dyspozytor.objects.create(imieDyspozytora='Jan', nazwiskoDyspozytora='Kowalski')


@pytest.fixture
def driver(db):
    return Kierowca.objects.create(imieKierowcy='Anna', nazwiskoKierowcy='Nowak')


@pytest.fixture
def customer(db):
    return Klient.objects.create(imieKlienta='Maria', nrTelefonu='123456789')


@pytest.fixture
def ride(dispatcher, driver, customer):
    return Usluga.objects.create(
        statusRealizacji=Usluga.W_TRAKCIE,
        idDyspozytora=dispatcher,
        idKierowcy=driver,
        idKlienta=customer,
        szerokoscGeoCelu=53.77,
        dlugoscGeoCelu=20.49,
    )
