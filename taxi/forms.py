from django import forms


class ClientInputForm(forms.Form):

    # name = forms.CharField(
    #     label='Klient',
    #     max_length=50,
    #     # widget=forms.TextInput(attrs={'class': 'form-control'}),
    # )
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