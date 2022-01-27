"""Mobile View of client."""

# Create your views here.
from mobile.forms import AcceptMobileForm
from django.views.generic import FormView
from django.views.generic import TemplateView


class ClientMobileView(FormView):

    template_name = 'mobile-app.html'
    form_class = AcceptMobileForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class SearchForDriverView(TemplateView):

    template_name = 'mobile-app.html'