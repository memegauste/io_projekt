from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from mobile.utils import state_dict
from taxi.models import Dyspozytor, Kierowca, Klient, Usluga

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('url_name', ['taxi:index', 'mobile:index'])
def test_pages_render_without_initial_data(client, url_name):
    assert client.get(reverse(url_name)).status_code == 200


def test_dispatcher_from_url_is_used_in_context_and_form(client, dispatcher):
    selected = Dyspozytor.objects.create(imieDyspozytora='Ewa', nazwiskoDyspozytora='Lis')
    response = client.get(reverse('taxi:index', kwargs={'pk': selected.pk}))
    assert response.context['dyspozytor'] == selected
    assert response.context['form'].initial['idDyspozytora'] == selected.pk


def test_default_dispatcher_is_first_record(client, dispatcher):
    response = client.get(reverse('taxi:index'))
    assert response.context['dyspozytor'] == dispatcher


def test_mobile_page_uses_driver_from_url(client, driver):
    selected = Kierowca.objects.create(imieKierowcy='Ewa', nazwiskoKierowcy='Lis')
    response = client.get(reverse('mobile:index', kwargs={'driver': selected.pk}))
    assert response.context['current_driver'] == selected.pk


def test_mobile_page_defaults_to_first_driver(client, driver):
    assert client.get(reverse('mobile:index')).context['current_driver'] == driver.pk


def test_robots_is_served_as_plain_text(client):
    response = client.get(reverse('taxi:robots'))
    assert response.status_code == 200
    assert response['Content-Type'].startswith('text/plain')
    assert b'User-agent: *' in response.content


def test_empty_driver_list_returns_success(client):
    response = client.get(reverse('taxi:load_drivers'))
    assert response.status_code == 200
    assert response.json()['is_finished'] is True
    assert 'Brak kierowców' in response.json()['html']


def test_driver_list_renders_names_and_status(client, driver):
    response = client.get(reverse('taxi:load_drivers'))
    assert str(driver) in response.json()['html']
    assert 'Niedostępny' in response.json()['html']


def test_available_drivers_exclude_busy_expired_and_offline(client, driver, ride):
    available = Kierowca.objects.create(imieKierowcy='Ewa', nazwiskoKierowcy='Lis')
    expired = Kierowca.objects.create(imieKierowcy='Piotr', nazwiskoKierowcy='Kot')
    offline = Kierowca.objects.create(imieKierowcy='Jan', nazwiskoKierowcy='Nowak')
    state_dict[driver.pk] = state_dict[available.pk] = timezone.now()
    state_dict[expired.pk] = timezone.now() - timedelta(minutes=6)
    response = client.get(reverse('taxi:load_available_drivers'))
    html = response.json()['html']
    assert str(available) in html
    for excluded in (driver, expired, offline):
        assert str(excluded) not in html


def test_available_driver_list_handles_no_online_drivers(client, driver):
    response = client.get(reverse('taxi:load_available_drivers'))
    assert 'Brak dostępnych kierowców' in response.json()['html']


def booking_data(dispatcher, driver):
    return {
        'idDyspozytora': dispatcher.pk,
        'imieKlienta': 'Maria',
        'nrTelefonu': '123456789',
        'adres': 'Olsztyn',
        'kierowcy': driver.pk,
        'lat': 53.77,
        'long': 20.49,
    }


def test_dispatcher_creates_customer_and_ride(client, dispatcher, driver):
    state_dict[driver.pk] = timezone.now()
    response = client.post(reverse('taxi:index'), booking_data(dispatcher, driver))
    assert response.json() == {'is_finished': True}
    ride = Usluga.objects.get()
    assert ride.idKierowcy == driver
    assert ride.idDyspozytora == dispatcher
    assert ride.idKlienta.imieKlienta == 'Maria'
    assert ride.idKlienta.nrTelefonu == '123456789'
    assert ride.statusRealizacji == Usluga.W_TRAKCIE
    assert (ride.szerokoscGeoCelu, ride.dlugoscGeoCelu) == (53.77, 20.49)


@pytest.mark.parametrize('state', ['offline', 'expired', 'busy'])
def test_dispatcher_cannot_book_unavailable_driver(client, dispatcher, driver, customer, state):
    if state == 'expired':
        state_dict[driver.pk] = timezone.now() - timedelta(minutes=6)
    if state == 'busy':
        state_dict[driver.pk] = timezone.now()
        Usluga.objects.create(
            statusRealizacji=Usluga.W_TRAKCIE, idDyspozytora=dispatcher,
            idKierowcy=driver, idKlienta=customer, szerokoscGeoCelu=0, dlugoscGeoCelu=0,
        )
    original_counts = (Klient.objects.count(), Usluga.objects.count())
    response = client.post(reverse('taxi:index'), booking_data(dispatcher, driver))
    assert response.json()['is_finished'] is False
    assert 'kierowcy' in response.json()['errors']
    assert (Klient.objects.count(), Usluga.objects.count()) == original_counts


def test_invalid_booking_returns_errors_without_creating_records(client):
    response = client.post(reverse('taxi:index'), {})
    assert response.json()['is_finished'] is False
    assert 'nrTelefonu' in response.json()['errors']
    assert not Klient.objects.exists()
    assert not Usluga.objects.exists()


def test_driver_heartbeat_updates_presence(client, driver):
    before = timezone.now()
    response = client.post(reverse('mobile:add_to_state'), {'driverId': driver.pk})
    assert response.json() == {'is_finished': True}
    assert before <= state_dict[driver.pk] <= timezone.now()


def test_driver_heartbeat_returns_active_ride(client, driver, ride):
    response = client.post(reverse('mobile:add_to_state'), {'driverId': driver.pk})
    assert response.json() == {
        'is_finished': True, 'lat': 53.77, 'long': 20.49, 'client_info': 'Maria 123456789',
    }


def test_driver_heartbeat_ignores_completed_rides(client, driver, ride):
    ride.statusRealizacji = Usluga.ZAKONCZONO
    ride.save()
    response = client.post(reverse('mobile:add_to_state'), {'driverId': driver.pk})
    assert response.json() == {'is_finished': True}


@pytest.mark.parametrize('driver_id', [
    None, '', '0', '-1', 'abc', '1.5', '2147483648', '9' * 5000, '²',
])
def test_driver_heartbeat_rejects_invalid_ids(client, driver_id):
    payload = {} if driver_id is None else {'driverId': driver_id}
    response = client.post(reverse('mobile:add_to_state'), payload)
    assert response.status_code == 400
    assert response.json() == {'is_finished': False}
    assert state_dict == {}


def test_driver_heartbeat_rejects_nonexistent_driver(client):
    response = client.post(reverse('mobile:add_to_state'), {'driverId': 12345})
    assert response.status_code == 404
    assert state_dict == {}


def test_driver_heartbeat_requires_post(client):
    response = client.get(reverse('mobile:add_to_state'))
    assert response.status_code == 405
    assert state_dict == {}
