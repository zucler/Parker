import os
import sys
from contextlib import closing

from selenium.webdriver import PhantomJS

sys.path.append('/carparker')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parker.settings")

import parker.wsgi
from parker.models import Parking, RateType, RatePrice
from django.conf import settings

carparkings = Parking.objects.all()
# carparkings = Parking.objects.filter(parkingID=7) # use for tests
for carpark in carparkings:
    url = carpark.uri
    with closing(PhantomJS()) as browser:
        browser.get(url)

        # store it as string variable
        with open(settings.HTML_CACHE_DIRECTORY + "/carparkID_" + str(carpark.parkingID) + ".html", "wb") as out_file:
            out_file.write(browser.page_source.encode('utf-8'))
