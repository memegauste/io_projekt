"""Mobile View of client."""

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
@require_POST
def add_driver_to_state(request):
    driver_id = request.POST.get('driverId', '')
    # Bound the value to the positive 32-bit AutoField range before querying.
    if not driver_id.isascii() or not driver_id.isdecimal() or len(driver_id) > 10:
        return JsonResponse({'is_finished': False}, status=400)
    driver_id = int(driver_id)
    if not 0 < driver_id <= 2147483647:
        return JsonResponse({'is_finished': False}, status=400)
    if not Kierowca.objects.filter(pk=driver_id).exists():
        return JsonResponse({'is_finished': False}, status=404)

    response_data = {'is_finished': True}
    usluga = Usluga.objects.filter(
        statusRealizacji=Usluga.W_TRAKCIE,
        idKierowcy=driver_id).last()
    if usluga:
        response_data.update({
            'lat': usluga.szerokoscGeoCelu,
            'long': usluga.dlugoscGeoCelu,
            'client_info': str(usluga.idKlienta),
        })
    state_dict[driver_id] = timezone.now()
    return JsonResponse(response_data)
