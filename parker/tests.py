__author__ = 'mpak'
import os
from decimal import *

from django.test import TestCase
from django.conf import settings

from parker.models import Parking, RateType, RatePrice
from parker.classes.core.utils import Utils


class WilsonsRateParserTest(TestCase):
    fixtures = ['parker.json']

    def test_main(self):
        carparks = Parking.objects.all()

        for carpark in carparks:
            carpark_rates, html = self._get_rates(carpark)

            for section_name in carpark_rates:
                self._validate_section(section_name, carpark_rates[section_name])

    def _validate_section(self, section_name, section_data):
        # Early Bird and Super Early Bird
        if Utils.string_found("Early Bird", section_name):
            self._validate_section_data(section_data=section_data, rate_types_expected=["flat"], days_expected=True)

        if section_name == 'Night':
            self._validate_section_data(section_data=section_data, rate_types_expected=["flat"], days_expected=True)

        if section_name == 'Weekend':
            self._validate_section_data(section_data=section_data, rate_types_expected=["flat", "hourly"],
                                        days_expected=True)

        if section_name == 'Casual':
            self._validate_section_data(section_data=section_data, rate_types_expected=["hourly"], days_expected=False)

    def _validate_section_data(self, section_data, rate_types_expected, days_expected):
        for field_name in section_data:
            field_value = section_data[field_name]

            if Utils.string_has_partial_match_in_list(["start", "end"], field_name):
                self._validate_time(field_value)

            if field_name == "prices":
                self._validate_prices(field_value)

            if field_name == "rate_type":
                if field_value not in rate_types_expected:
                    raise Exception("Invalid rate type")

            if field_name == "days":
                if days_expected:
                    self._validate_days(section_data[field_name])
                else:
                    self.assertEqual("", field_value)

    def _validate_days(self, days):
        if type(days) is not list:
            raise Exception("Invalid days type")

        for day in days:
            self.assertTrue(Utils.is_number(day))

    def _validate_prices(self, prices):
        if type(prices) is dict:
            for time_period in prices:
                self._validate_prices(prices[time_period])
        else:
            self.assertTrue(Utils.is_number(prices))

    def _validate_time(self, time_string):
        time_array = time_string.split(":")

        self.assertEquals(2, len(time_array))

        self.assertTrue(Utils.is_number(time_array[0]))
        self.assertTrue(Utils.is_number(time_array[1]))

    def _get_rates(self, carpark: Parking):
        html_file = os.path.join(settings.HTML_CACHE_DIRECTORY, "carparkID_" + str(carpark.parkingID) + ".html")
        rates_file = open(html_file, "rb")
        rates_bytes = rates_file.read()
        rates_html = rates_bytes.decode("utf-8")
        rates_file.close()

        mod = __import__("parker.classes.custom." + carpark.parking_type.lower() + ".rates_retriever",
                         fromlist=['RatesRetriever'])
        RatesRetriever = getattr(mod, 'RatesRetriever')
        # store it as string variable
        parser = RatesRetriever()
        rates = parser.get_rates(rates_html)
        return rates, rates_html

    def _update_rates(selfs, carpark, html):
        mod = __import__("parker.classes.custom.wilson.rates_retriever",
                         fromlist=['RatesRetriever'])

        RatesRetriever = getattr(mod, 'RatesRetriever')
        parser = RatesRetriever()
        parser.update_rates(carpark, html)

    def _get_stored_prices(self, carpark, rate_label, rate_type, day_of_week=-1):
        # rates are QuerySets
        rates = RateType.objects.filter(parkingID=carpark, label=rate_label, rate_type=rate_type)

        if day_of_week > -1:
            rates = rates.filter(day_of_week=day_of_week)

        prices = []
        for rate in rates:
            prices.append(RatePrice.objects.filter(rateID=rate).order_by('duration'))

        return prices

    def _assert_saved_rates(self, carpark, expected_result):
        # Check casual rates stored in DB
        casual_prices = self._get_stored_prices(carpark, "Casual", "hourly", 0)

        for price in casual_prices[0]:
            self.assertEquals(price.price, Decimal(expected_result['Casual']['prices'][price.duration]))

        # Check early bird rates stored in DB
        early_bird_prices = self._get_stored_prices(carpark, "Early Bird", "flat")
        for single_day_price in early_bird_prices:
            self.assertEquals(single_day_price[0].price, Decimal(expected_result['Early Bird']['prices']))

        # Check super early bird rates stored in DB
        super_early_bird_prices = self._get_stored_prices(carpark, "Super Early Bird", "flat")
        for single_day_price in super_early_bird_prices:
            self.assertEquals(single_day_price[0].price, Decimal(expected_result['Super Early Bird']['prices']))

        # Check super early bird rates stored in DB
        # night_prices = self._get_stored_prices(carpark, "Night", "flat")
        # for single_day_price in night_prices:
        #     self.assertEquals(single_day_price[0].price, Decimal(expected_result['Night']['rates']['prices'][0]))

        # Check weekend rates stored in DB
        weekend_prices = self._get_stored_prices(carpark, "Weekend", "flat")
        for single_day_price in weekend_prices:
            self.assertEquals(single_day_price[0].price, Decimal(expected_result['Weekend']['prices']))
