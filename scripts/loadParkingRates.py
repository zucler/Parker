import os
import sys
from contextlib import closing

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

import parker.wsgi
from parker.classes.core.utils import Utils
from parker.models import Parking, RateType, RatePrice

sys.path.append('/srv/prod/carparker')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parker.settings")

# carparkings = Parking.objects.all()
carparkings = Parking.objects.filter(parkingID=7)
for carpark in carparkings:
    mod = __import__("parker.classes.custom." + carpark.parking_type.lower() + ".rates_retriever", fromlist=['RatesRetriever'])
    RatesRetriever = getattr(mod, 'RatesRetriever')
    url = carpark.uri
    # use firefox to get page with javascript generated content
    with closing(Firefox()) as browser:
        browser.get(url)
        # wait for the page to load
        WebDriverWait(browser, timeout=10).until(
                lambda x: x.find_element_by_class_name('rates'))
        # store it as string variable
        parser = RatesRetriever()
        parser._update_rates(carpark, browser.page_source)
        exit()

