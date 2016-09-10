import os
import sys

import parker.wsgi
from parker.models import Parking, RateType, RatePrice
from django.conf import settings

sys.path.append('/srv/prod/carparker')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parker.settings")

for html_file in os.listdir(settings.HTML_CACHE_DIRECTORY):
    if html_file.endswith(".html"):
        rates_file = open(os.path.join(settings.HTML_CACHE_DIRECTORY, html_file), "r")
        rates_html = rates_file.read()
        rates_file.close()

        carparkID = html_file[settings.HTML_FILE_PREFIX_LENGTH:-settings.HTML_FILE_SUFFIX_LENGTH]
        carpark = Parking.objects.get(parkingID=carparkID)
        mod = __import__("parker.classes.custom." + carpark.parking_type.lower() + ".rates_retriever",
                         fromlist=['RatesRetriever'])
        RatesRetriever = getattr(mod, 'RatesRetriever')
        # store it as string variable
        parser = RatesRetriever()
        parser.update_rates(carpark, rates_html)
