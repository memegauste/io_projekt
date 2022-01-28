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
from taxi.forms import ClientInputForm
from taxi.forms import DriversForm
from taxi.models import Kierowca
from taxi.models import Usluga
from taxi.utils import get_sorted_driver_instances


class DyspozytorView(FormView):  # noqa: D101

    template_name = 'index.html'
    form_class = ClientInputForm

    def form_valid(self, form):
        return JsonResponse({
            'test': True
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
        usluga__in=Usluga.objects.filter(statusRealizacji__in=[Usluga.ZAJETY]))
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