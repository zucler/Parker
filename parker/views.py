from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Parking, RateType, RatePrice

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

