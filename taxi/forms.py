from django import forms
from taxi.models import Kierowca
from taxi.utils import get_sorted_driver_instances


class DyspozytorForm(forms.Form):

    idDyspozytora = forms.IntegerField(
        widget=forms.HiddenInput,
    )
    phone = forms.CharField(
        label='Nr Telefonu',
        max_length=9,
        # widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    address = forms.CharField(
        label='Adres',
        max_length=50,
        # widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    drivers = forms.ModelChoiceField(
        queryset=Kierowca.objects.none(),
        widget=forms.HiddenInput,
    )
    long = forms.FloatField(
        widget=forms.HiddenInput,
    )
    lat = forms.FloatField(
        widget=forms.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        """Dyspozytor form init method."""
        drivers_ids = kwargs.pop('drivers_ids', None)
        super().__init__(*args, **kwargs)
        if drivers_ids:
            drivers = get_sorted_driver_instances(drivers_ids)
            self.fields['drivers'].queryset = drivers



class DriversForm(forms.Form):

    drivers = forms.ModelChoiceField(
        queryset=Kierowca.objects.none(),
        widget=forms.RadioSelect,
    )

    def __init__(self, drivers_ids=[], *args, **kwargs):
        """Drivers Form init method."""
        super().__init__(*args, **kwargs)
        if drivers_ids:
            drivers = get_sorted_driver_instances(drivers_ids)
            self.fields['drivers'].queryset = drivers