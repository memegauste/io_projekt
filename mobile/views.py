"""Mobile View of client."""

# Create your views here.
from mobile.forms import AcceptMobileForm
from django.views.generic import FormView


class ClientMobileView(FormView):

    template_name = 'mobile-app.html'
    form_class = AcceptMobileForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)