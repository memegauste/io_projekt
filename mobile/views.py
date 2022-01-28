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
from taxi.models import Kierowca, Usluga


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
    if request.POST['driverId'] != 0:
        response_data = {'is_finished': True}
        usluga = Usluga.objects.filter(
            statusRealizacji=Usluga.W_TRAKCIE,
            idKierowcy=request.POST['driverId']).last()
        if usluga:
            response_data.update({
                'lat': usluga.szerokoscGeoCelu,
                'long': usluga.dlugoscGeoCelu,
            })
        state_dict[int(request.POST['driverId'])] = timezone.now()
        return JsonResponse(response_data)
    return JsonResponse({'is_finished': False})