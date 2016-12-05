import os
import pprint
import sys
import django
from django.db.models.query_utils import Q

sys.path.append('/carparker')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parker.settings.default")
django.setup()


from django.db import models

from parker.models.common import Parking
from parker.classes.custom.wilson.parking_list_retriever import AllParkingsList
from parker.settings.wilson import webHome


from django.conf import settings


for html_file in os.listdir(settings.HTML_CACHE_DIRECTORY):
    if html_file.endswith("wilson_all_parkings.html"):
        list_file = open(os.path.join(settings.HTML_CACHE_DIRECTORY, html_file), "rb")
        list_bytes = list_file.read()
        list_html = list_bytes.decode('utf-8')
        list_file.close()

        parser = AllParkingsList()
        urls = parser.get_list(list_html)

        fullUrls = [webHome + '/park/' + url for url in urls]

        alreadyThere = Parking.objects.filter(Q(uri__in=fullUrls))

        # Remove from url list all parkings already in database
        for parking in alreadyThere:
            fullUrls.remove(parking.uri)

        #notThere = Parking.objects.filter(~Q(uri__in=fullUrls))
        #notThere = Parking.objects.exclude(uri__in=fullUrls)
        # TODO: Disable the rest parkings in database (Implement enable field)

        # Add the rest of url list to database
        for fullUrl in fullUrls:
            p = Parking(uri=fullUrl)
            p.save()

        pprint.pprint(fullUrls)
