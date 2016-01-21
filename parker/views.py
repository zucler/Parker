from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse
from django.template import loader
from django.views import generic

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Parking, RateType, RatePrice
from .constants import GOOGLE_MAPS_API_KEY

import django.http
from rest_framework import viewsets
from rest_framework.decorators import detail_route

from .dbhelpers import geo_search
from parker.serializers import ParkingSerializer


class JSONResponse(HttpResponse):
    """An HttpResponse that renders its content into JSON."""
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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


def search_index(request):
    """Searching for parkings in given boundary"""
    template = loader.get_template("parker/search.html")
    context = { "google_maps_api_key": GOOGLE_MAPS_API_KEY, }
    return HttpResponse(template.render(context, request))


class ParkingViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()

    @detail_route(methods=['get'], url_path='parkings')
    def find_parkings_by_latlong(self, request: HttpRequest, pk=None):
        getdict = request.GET
        minlat = getdict.get("minlat", None)
        maxlat = getdict.get("maxlat", None)
        minlong = getdict.get("minlong", None)
        maxlong = getdict.get("maxlong", None)

        queryset = geo_search(minlat, maxlat, minlong, maxlong)

        serializer = ParkingSerializer(queryset, many=True)
        return Response(serializer.data)