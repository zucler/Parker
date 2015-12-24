__author__ = 'Maxim Pak'

import parker.wsgi

from contextlib import closing

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

from parker.parser import WillsonsRatesParser
from parker.models import Parking, RateType, RatePrices


parkings = Parking.objects.all()
for carpark in parkings:
    url = carpark.uri
    # use firefox to get page with javascript generated content
    with closing(Firefox()) as browser:
        browser.get(url)
        # wait for the page to load
        WebDriverWait(browser, timeout=10).until(
            lambda x: x.find_element_by_class_name('rates'))
        # store it to string variable
        page_source = browser.page_source
        parser = WillsonsRatesParser()
        rates = parser.get_prices_information(page_source)
        print(rates.rates)
