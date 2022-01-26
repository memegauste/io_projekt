"""Mainapp views file."""

# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):

    template_name = 'index.html'


class RobotsView(TemplateView):

    template = 'robots.txt'
    content_type = 'text/plain'
