from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from mobile.utils import state_dict
from taxi.models import Dyspozytor, Kierowca, Klient, Usluga


@pytest.mark.parametrize(('instance', 'expected'), [
    (Klient(imieKlienta='Maria', nrTelefonu='123456789'), 'Maria 123456789'),
    (Dyspozytor(imieDyspozytora='Jan', nazwiskoDyspozytora='Kowalski'), 'Jan Kowalski'),
    (Kierowca(imieKierowcy='Anna', nazwiskoKierowcy='Nowak'), 'Anna Nowak'),
    (Usluga(idUsluga=42), 'Usługa o id 42'),
])
def test_model_display_name(instance, expected):
    assert str(instance) == expected


@pytest.mark.parametrize(('minutes_ago', 'expected'), [
    (None, 'Niedostępny'),
    (0, 'Dostępny'),
    (4, 'Dostępny'),
    (5, 'Niedostępny'),
    (6, 'Niedostępny'),
])
def test_driver_status_expires_at_logout_boundary(driver, settings, minutes_ago, expected):
    settings.AUTOLOGOUT_MINUTES = 5
    now = timezone.now()
    if minutes_ago is not None:
        state_dict[driver.pk] = now - timedelta(minutes=minutes_ago)
    with patch('taxi.models.timezone.now', return_value=now):
        assert expected in driver.get_status()


def test_busy_driver_takes_priority_over_online_state(ride, driver):
    state_dict[driver.pk] = timezone.now()
    assert 'Zajęty' in driver.get_status()


def test_completed_ride_does_not_keep_driver_busy(ride, driver):
    ride.statusRealizacji = Usluga.ZAKONCZONO
    ride.save()
    state_dict[driver.pk] = timezone.now()
    assert 'Dostępny' in driver.get_status()


def test_logout_timeout_can_be_configured(driver, settings):
    settings.AUTOLOGOUT_MINUTES = 1
    state_dict[driver.pk] = timezone.now() - timedelta(minutes=2)
    assert 'Niedostępny' in driver.get_status()
