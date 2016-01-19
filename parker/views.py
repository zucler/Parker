from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.views import generic

from .models import Parking, RateType, RatePrice
from .constants import GOOGLE_MAPS_API_KEY


def index(request):
    return HttpResponse("Hello, world. We are at the carparker index")


def test(request):
    template_name = "parker/test_search.html"


class DetailView(generic.DetailView):
    model = Parking
    template_name = 'parker/details.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['rates'] = RateType.objects.filter(parkingID=self.object.parkingID)

        return context


def search(request):
    "Searching for parkings in given boundary"
    template = loader.get_template("parker/search.html")
    context = { "google_maps_api_key": GOOGLE_MAPS_API_KEY }
    return HttpResponse(template.render(context, request))