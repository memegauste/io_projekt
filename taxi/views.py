"""Taxi views file."""

# Create your views here.
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView

from taxi.forms import ClientInputForm
from taxi.models import Kierowca


class IndexView(FormView):  # noqa: D101

    template_name = 'index.html'
    form_class = ClientInputForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Kierowca.objects.all()
        return context


class RobotsView(TemplateView):  # noqa: D101

    template = 'robots.txt'
    content_type = 'text/plain'


@csrf_exempt
def load_drivers(request):
    template = 'drivers.html'
    body = render_to_string(
        template,
        {'drivers': Kierowca.objects.all()},
    )
    return JsonResponse({
        'is_finished': True,
        'html': body,
    })