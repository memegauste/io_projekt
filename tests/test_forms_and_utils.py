import pytest
from django import forms
from django.utils import timezone

from mobile.forms import AcceptMobileForm
from mobile.utils import state_dict
from taxi.forms import DriversForm, DyspozytorForm
from taxi.models import Kierowca
from taxi.utils import build_error_dict, get_sorted_driver_instances


def test_empty_driver_list_does_not_query_database(db, django_assert_num_queries):
    with django_assert_num_queries(0):
        assert list(get_sorted_driver_instances([])) == []


def test_online_drivers_are_first_and_input_order_is_preserved(driver):
    second = Kierowca.objects.create(imieKierowcy='Piotr', nazwiskoKierowcy='Lis')
    third = Kierowca.objects.create(imieKierowcy='Ewa', nazwiskoKierowcy='Kot')
    state_dict[third.pk] = timezone.now()
    assert list(get_sorted_driver_instances([second.pk, third.pk, driver.pk])) == [
        third, second, driver,
    ]


def test_missing_driver_ids_are_ignored(driver):
    assert list(get_sorted_driver_instances([driver.pk + 1000, driver.pk])) == [driver]


@pytest.mark.parametrize('form_class', [DriversForm, DyspozytorForm])
def test_driver_choices_are_empty_by_default(db, form_class):
    assert list(form_class().fields['kierowcy'].queryset) == []


@pytest.mark.parametrize('form_class', [DriversForm, DyspozytorForm])
def test_driver_choices_are_limited_to_provided_ids(driver, form_class):
    Kierowca.objects.create(imieKierowcy='Piotr', nazwiskoKierowcy='Lis')
    form = form_class(drivers_ids=[driver.pk])
    assert list(form.fields['kierowcy'].queryset) == [driver]


def test_driver_form_rejects_a_driver_outside_choices(driver):
    form = DriversForm(data={'kierowcy': driver.pk}, drivers_ids=[])
    assert not form.is_valid()
    assert 'kierowcy' in form.errors


def test_error_dict_contains_field_labels_and_non_field_errors():
    class ExampleForm(forms.Form):
        name = forms.CharField(label='Imię')

        def clean(self):
            super().clean()
            raise forms.ValidationError('Błąd całego formularza')

    form = ExampleForm(data={})
    errors = build_error_dict(form)
    assert errors['name']['label'] == 'Imię'
    assert errors['name']['errors'] == form.errors['name']
    assert errors['other']['label'] == 'Inne błędy'
    assert errors['other']['errors'] == ['Błąd całego formularza']


def test_valid_form_has_no_error_dict():
    assert build_error_dict(AcceptMobileForm(data={'target': 'Olsztyn'})) == {}


@pytest.mark.parametrize('data', [{}, {'target': 'x' * 51}])
def test_mobile_form_rejects_missing_or_too_long_target(data):
    assert not AcceptMobileForm(data=data).is_valid()
