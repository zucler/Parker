__author__ = 'Maxim Pak'

from contextlib import closing

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

import parker.wsgi
from parker.models import Parking, RateType
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
        page_source = browser.page_source
        parser = WillsonsRatesParser()
        rates = parser.get_prices_information(page_source)
        # save rates into DB
        for rate_name, rate_type in rates.types.items():
            carpark_rate_type = RateType(parkingID=carpark, label=rate_name, type=rate_type)
            # @TODO: Load this data from website
            # Hardcoded data to allow to finish the task
            if rate_name == "Early Bird":
                carpark_rate_type.start_time = "07:00"
                carpark_rate_type.end_time = "09:00"
                carpark_rate_type.day_of_week = "Mon"
            elif rate_name == "Night":
                carpark_rate_type.start_time = "18:00"
                carpark_rate_type.end_time = "23:59"
                carpark_rate_type.day_of_week = "Mon"
            elif rate_name == "Casual":
                carpark_rate_type.start_time = "09:00"
                carpark_rate_type.end_time = "18:00"
                carpark_rate_type.day_of_week = "Mon"
            elif rate_name == "Weekend":
                carpark_rate_type.start_time = "06:00"
                carpark_rate_type.end_time = "23:59"
                carpark_rate_type.day_of_week = "Sun"

                # carpark_rate_type.save()
                # print("Carpark rate id is " + str(carpark_rate_type.rateID))
