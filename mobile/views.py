"""Mobile View of client."""

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from mobile.forms import AcceptMobileForm
from django.views.generic import FormView
from django.views.generic import TemplateView

# Set temporary memory variable.
from mobile.utils import state_dict
from taxi.models import Kierowca


class ClientMobileView(FormView):

    template_name = 'mobile-app.html'
    form_class = AcceptMobileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_driver'] = getattr(Kierowca.objects.first(), 'idKierowcy', 0)
        if 'driver' in self.kwargs:
            context['current_driver'] = getattr(Kierowca.objects.filter(
                idKierowcy=self.kwargs['driver']).first(), 'idKierowcy', 0)
        return context


class SearchForDriverView(TemplateView):

    template_name = 'mobile-app.html'


@csrf_exempt
def add_driver_to_state(request):
    try:
        driver = Kierowca.objects.get(idKierowcy=request.POST['driverId'])
        driver.lat = request.POST['lat']
        driver.long = request.POST['long']
        driver.save()
    except (Kierowca.DoesNotExist, KeyError) as e:
        pass
    if request.POST['driverId'] != 0:
        state_dict[int(request.POST['driverId'])] = timezone.now()
        return JsonResponse({'is_finished': True})
    return JsonResponse({'is_finished': False})