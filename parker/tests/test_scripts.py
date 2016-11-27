import os

from django.test import TestCase
from django.conf import settings

from parker.models.common import Parking, RateType, RatePrice
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
