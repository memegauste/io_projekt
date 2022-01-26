"""Mainapp views file."""

# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):  # noqa: D101

    template_name = 'index.html'


class RobotsView(TemplateView):  # noqa: D101

    template = 'robots.txt'
    content_type = 'text/plain'
