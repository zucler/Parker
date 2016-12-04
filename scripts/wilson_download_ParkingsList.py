import os
import sys
from contextlib import closing

from selenium.webdriver import PhantomJS

sys.path.append('/carparker')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parker.settings.default")

import parker.wsgi
from parker.models.common import Parking
from django.conf import settings
from parker.settings.wilson import webHome, parkingsListPath

# carparkings = Parking.objects.all()
# carparkings = Parking.objects.filter(parkingID=7) # use for tests

wilsonWebHome = webHome
wilsonAllListPath = parkingsListPath

url = wilsonWebHome + wilsonAllListPath
with closing(PhantomJS()) as browser:
    browser.get(url)

    # store it as string variable
    with open(settings.HTML_CACHE_DIRECTORY + "/wilson_all_parkings.html", "wb") as out_file:
        out_file.write(browser.page_source.encode('utf-8'))
