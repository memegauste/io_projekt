from django import forms


class AcceptMobileForm(forms.Form):

    target = forms.CharField(
        label='Adres docelowy',
        max_length=50,
    )