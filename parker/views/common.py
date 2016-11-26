from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse
from django.template import loader
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from parker.models.common import Parking, RateType, RatePrice
from parker.models.helpers import geo_search_all_models
from parker.models.serializers import ParkingSerializer
from parker.constants import GOOGLE_MAPS_API_KEY




class JSONResponse(HttpResponse):
    """An HttpResponse that renders its content into JSON."""
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    return HttpResponse("Hello, world. We are at the carparker index")


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
        s = getdict.get("s", None)
        w = getdict.get("w", None)
        n = getdict.get("n", None)
        e = getdict.get("e", None)

        try:
            geosearch = geo_search_all_models(s, w, n, e)
        except ValueError:
            raise

        # First we need to take Parking item.
        # Then when we know parkingID we should find all RateType with that ID.
        # Then we need to find all RatePrices with each found RateType.
        # So it is O(n^2) complexity

        # I'll try to use dict comprehensions:
        # x = { row.SITE_NAME : row.LOOKUP_TABLE for row in cursor }

        parkings = list(geosearch['parkings'])     # Here we have list of dicts
        rtype = geosearch['ratetype']
        rprice = geosearch['rateprice']

        for p_item in parkings:
            sub_ratetype = rtype.filter(parkingID=p_item.parkingID)
            for rt_item in sub_ratetype:
                rt_item.rateprice = list(rprice.filter(rateID=rt_item.rateID))
            p_item.ratetype = sub_ratetype

        serializer = ParkingSerializer(parkings, many=True)
        return JSONResponse(serializer.data)