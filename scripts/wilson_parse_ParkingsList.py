import os
import pprint
import sys
import django


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

        pprint.pprint(fullUrls)