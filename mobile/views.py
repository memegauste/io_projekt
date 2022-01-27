"""Mobile View of client."""

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from mobile.forms import AcceptMobileForm
from django.views.generic import FormView
from django.views.generic import TemplateView

# Set temporary memory variable.
from taxi.models import Kierowca

state_dict = {}


class ClientMobileView(FormView):

    template_name = 'mobile-app.html'
    form_class = AcceptMobileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_driver'] = getattr(Kierowca.objects.first(), 'idKierowcy', 0)
        return context


class SearchForDriverView(TemplateView):

    template_name = 'mobile-app.html'


@csrf_exempt
def add_driver_to_state(request):
    if request.POST['driverId'] != 0:
        state_dict[request.POST['driverId']] = timezone.now()
        return JsonResponse({'is_finished': True})
    return JsonResponse({'is_finished': False})