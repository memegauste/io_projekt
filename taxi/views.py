"""Taxi views file."""

# Create your views here.
from datetime import timedelta

from django.db.models import Case, When
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView

from mobile.utils import state_dict
from taxi.forms import ClientInputForm
from taxi.models import Kierowca
from taxi.models import Usluga


class DyspozytorView(FormView):  # noqa: D101

    template_name = 'index.html'
    form_class = ClientInputForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['drivers'] = Kierowca.objects.all()
    #     return context

    def form_valid(self, form):
        return JsonResponse({
            'test': True
        })


class RobotsView(TemplateView):  # noqa: D101

    template = 'robots.txt'
    content_type = 'text/plain'


@csrf_exempt
def load_drivers(request):
    get_drivers = []
    if request.POST['filter'] == 'all':
        drivers = Kierowca.objects.all()
    else:
        for key, value in state_dict.items():
            if value > timezone.now() - timedelta(minutes=5):
                get_drivers.append(key)
        drivers = Kierowca.objects.filter(
            idKierowcy__in=get_drivers,
        ).exclude(usluga__in=Usluga.objects.filter(statusRealizacji__in=[Usluga.ROZPOCZETO, Usluga.W_TRAKCIE]))
    ids = list(drivers.values_list('idKierowcy', flat=True))
    ordered_ids = []
    for id in ids:
        if id in state_dict.keys():
            ordered_ids.append(id)
    [ordered_ids.append(id) for id in ids if id not in ordered_ids]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ordered_ids)])
    drivers = Kierowca.objects.filter(idKierowcy__in=ordered_ids).order_by(preserved)
    template = 'drivers.html'
    body = render_to_string(
        template,
        {'drivers': drivers},
    )
    return JsonResponse({
        'is_finished': True,
        'html': body,
    })