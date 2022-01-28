"""Taxi views file."""

# Create your views here.
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView
from mobile.utils import state_dict
from taxi.forms import DyspozytorForm
from taxi.forms import DriversForm
from taxi.models import Kierowca, Dyspozytor
from taxi.models import Usluga
from taxi.utils import build_error_dict
from taxi.utils import get_sorted_driver_instances


class DyspozytorView(FormView):  # noqa: D101

    template_name = 'index.html'
    form_class = DyspozytorForm

    def get_initial(self):  # noqa: D102
        initial = super().get_initial()
        initial['dyspozytor'] = Dyspozytor.objects.first()
        if 'dys_id' in self.kwargs:
            initial['dyspozytor'] = Dyspozytor.objects.filter(
                idDyspozytora=self.kwargs['dys_id'])
        return initial

    def get_form_kwargs(self):
        """Additional method for passing kwarts to validation."""
        kwargs = super().get_form_kwargs()
        get_drivers = []
        for key, value in state_dict.items():
            if value > timezone.now() - timedelta(minutes=getattr(settings, 'AUTOLOGOUT_MINUTES', 5)):
                get_drivers.append(key)
        available_drivers = Kierowca.objects.filter(idKierowcy__in=get_drivers).exclude(
            usluga__in=Usluga.objects.filter(statusRealizacji__in=[Usluga.W_TRAKCIE]))
        available_ids = list(available_drivers.values_list('idKierowcy', flat=True))
        kwargs['drivers_ids'] = available_ids
        return kwargs

    def form_valid(self, form):
        """Do the stuff if form is valid."""
        Usluga.objects.create(
            statusRealizacji=Usluga.W_TRAKCIE,
            idDyspozytora=form.cleaned_data['dyspozytorId'],
            idKierowcy=form.cleaned_data['driver'],
            dlugoscGeoCelu=form.cleaned_data['long'],
            szerokoscGeoCelu=form.cleaned_data['lat'],
        )
        return JsonResponse({'is_finished': True})

    def form_invalid(self, form):
        """Return json response with errors and form status."""
        return JsonResponse({
            'is_finished': False,
            'errors': build_error_dict(form),
        })


class RobotsView(TemplateView):  # noqa: D101

    template = 'robots.txt'
    content_type = 'text/plain'


@csrf_exempt
def load_drivers(request):
    all_drivers = Kierowca.objects.all()
    drivers = get_sorted_driver_instances(
        list(all_drivers.values_list('idKierowcy', flat=True)))
    list_body = render_to_string(
        'drivers.html',
        {'drivers': drivers},
    )
    return JsonResponse({
        'is_finished': True,
        'html': list_body,
    })


@csrf_exempt
def load_available_drivers(request):
    get_drivers = []
    for key, value in state_dict.items():
        if value > timezone.now() - timedelta(minutes=getattr(settings, 'AUTOLOGOUT_MINUTES', 5)):
            get_drivers.append(key)
    available_drivers = Kierowca.objects.filter(idKierowcy__in=get_drivers).exclude(
        usluga__in=Usluga.objects.filter(statusRealizacji__in=[Usluga.W_TRAKCIE]))
    available_ids = list(available_drivers.values_list('idKierowcy', flat=True))
    get_form = DriversForm(drivers_ids=available_ids)
    form_body = render_to_string(
        'drivers-radio.html',
        {'drivers_form': get_form}
    )
    return JsonResponse({
        'is_finished': True,
        'html': form_body,
    })