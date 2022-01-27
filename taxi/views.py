"""Taxi views file."""

# Create your views here.
from datetime import timedelta

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
    for key, value in state_dict.items():
        if value > timezone.now() - timedelta(minutes=5):
            get_drivers.append(key)
    if request.POST['filter'] == 'all':
        drivers = Kierowca.objects.all()
    else:
        drivers = Kierowca.objects.filter(
            id__in=get_drivers,
        ).exclude(usluga__in=Usluga.objects.filter(statusRealizacji__in=[Usluga.ROZPOCZETO, Usluga.W_TRAKCIE]))
    template = 'drivers.html'
    body = render_to_string(
        template,
        {'drivers': drivers},
    )
    return JsonResponse({
        'is_finished': True,
        'html': body,
    })