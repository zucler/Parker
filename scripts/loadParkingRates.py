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
carparkings = Parking.objects.filter(parkingID=4)
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
        parser.update_rates(browser.page_source)
        exit()
        # save rates into DB
        for rate_name, rate_data in rates.types.items():
            if rate_data['type'] == "Flat":
                for day_of_week in rate_data['days_range']:
                    save_carpark_rate = False
                    carpark_rate, created = RateType.objects.get_or_create(parkingID=carpark, label=rate_name,
                                                                           rate_type=rate_data['type'],
                                                                           day_of_week=day_of_week)

                    if carpark_rate.start_time != rate_data['start']:
                        carpark_rate.start_time = rate_data['start']
                        save_carpark_rate = True

                    if carpark_rate.end_time != rate_data['end']:
                        carpark_rate.end_time = rate_data['end']
                        save_carpark_rate = True

                    if save_carpark_rate:
                        carpark_rate.save()

                    carpark_rate_price, created = RatePrice.objects.get_or_create(rateID=carpark_rate, duration=0)
                    if carpark_rate_price != rates.rates[rate_name][day_of_week]:
                        carpark_rate_price.price = rates.rates[rate_name][day_of_week]
                        print(carpark_rate_price.price + " = " + rates.rates[rate_name][day_of_week])
                        carpark_rate_price.save()
            elif rate_data['type'] == "Hourly":
                carpark_rate, created = RateType.objects.get_or_create(parkingID=carpark, label=rate_name,
                                                                       rate_type=rate_data['type'],
                                                                       day_of_week=0)

                save_carpark_rate = False
                if carpark_rate.start_time != rate_data['start']:
                    carpark_rate.start_time = rate_data['start']
                    save_carpark_rate = True

                if carpark_rate.end_time != rate_data['end']:
                    carpark_rate.end_time = rate_data['end']
                    save_carpark_rate = True

                if save_carpark_rate:
                    carpark_rate.save()

                for price in rates.rates[rate_name].items():
                    carpark_rate_price, created = RatePrice.objects.get_or_create(rateID=carpark_rate,
                                                                                  duration=price[0])

                    if carpark_rate_price.price != price[1]:
                        carpark_rate_price.price = price[1]
                        carpark_rate_price.save()
