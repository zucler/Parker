__author__ = 'Maxim Pak'

import os
import sys
from contextlib import closing

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append('/srv/prod/carparker')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parker.settings")
import parker.wsgi
from parker.models import Parking, RateType, RatePrice
from parker.parser import WillsonsRatesParser

carparkings = Parking.objects.all()
for carpark in carparkings:
    url = carpark.uri
    # use firefox to get page with javascript generated content
    with closing(Firefox()) as browser:
        browser.get(url)
        # wait for the page to load
        WebDriverWait(browser, timeout=10).until(
                lambda x: x.find_element_by_class_name('rates'))
        # store it as string variable
        parser = WillsonsRatesParser()
        rates = parser.get_prices_information(browser.page_source)
        # save rates into DB
        for rate_name, rate_data in rates.types.items():
            if rate_data['type'] == "Flat":
                for day_of_week in rate_data['days_range']:
                    carpark_rate = RateType(parkingID=carpark, label=rate_name, type=rate_data['type'],
                                            day_of_week=day_of_week, start_time=rate_data['start'],
                                            end_time=rate_data['end'])
                    carpark_rate.save()

                    carpark_rate_price = RatePrice(rateID=carpark_rate, duration=0,
                                                   price=rates.rates[rate_name][day_of_week])
                    carpark_rate_price.save()
            elif rate_data['type'] == "Hourly":
                carpark_rate = RateType(parkingID=carpark, label=rate_name, type=rate_data['type'], day_of_week="",
                                        start_time=rate_data['start'], end_time=rate_data['end'])
                carpark_rate.save()

                for price in rates.rates[rate_name].items():
                    carpark_rate_price = RatePrice(rateID=carpark_rate, duration=price[0], price=price[1])
                    carpark_rate_price.save()
