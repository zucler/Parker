from django.test import TestCase
from parker.models.common import Parking
from parker.classes.core.utils import Utils


class WilsonRatesParserTest(TestCase):
    fixtures = ['parker.json']

    def test_rates_parser(self):
        """ Main test function """
        carparks = Parking.objects.all()

        for carpark in carparks:
            carpark_rates = Utils.get_rates(carpark)

            for section_name in carpark_rates:
                self.__validate_section(section_name, carpark_rates[section_name])

    def __validate_section(self, section_name: str, section_data: dict):
        """
        Validate a single Wilson rate section

        Args:
            section_name: e.g. Early Bird, Night, Weekend, etc
            section_data: dictionary containing all data retrieved by an HTML parser
        """
        if Utils.string_found("Early Bird", section_name):
            self.__validate_section_data(section_data=section_data, rate_types_expected=["flat"], days_expected=True)

        if section_name == 'Night':
            self.__validate_section_data(section_data=section_data, rate_types_expected=["flat"], days_expected=True)

        if section_name == 'Weekend':
            self.__validate_section_data(section_data=section_data, rate_types_expected=["flat", "hourly"],
                                         days_expected=True)

        if section_name == 'Casual':
            self.__validate_section_data(section_data=section_data, rate_types_expected=["hourly"], days_expected=False)

    def __validate_section_data(self, section_data: dict, rate_types_expected: list, days_expected: bool):
        """
        Validates data retrieved by Wilson Rates Parser for a single section

        Args:
            section_data: dictionary of section data retrieved
            rate_types_expected: list containing one or all of: flat, hourly
            days_expected: whether list of days is expected or not

        """
        for field_name in section_data:
            field_value = section_data[field_name]

            if Utils.string_has_partial_match_in_list(["start", "end"], field_name):
                self.__validate_time(field_value)

            if field_name == "prices":
                self.__validate_prices(field_value)

            if field_name == "rate_type":
                if field_value not in rate_types_expected:
                    raise Exception("Invalid rate type")

            if field_name == "days":
                if days_expected:
                    self.__validate_days(section_data[field_name])
                else:
                    self.assertEqual("", field_value)

    def __validate_days(self, days: list):
        """
        Validate rate days

        Args:
            days: list of digits following rule 1 <= day <= 7

        Returns:

        """
        if type(days) is not list:
            raise Exception("Invalid days type")

        for day in days:
            self.assertTrue(Utils.is_number(day))
            self.assertTrue(day <= 7)
            self.assertTrue(day >= 1)

    def __validate_prices(self, prices: dict):
        """
        Validate rate prices

        Args:
            prices: dictionary of prices

        """
        if type(prices) is dict:
            for time_period in prices:
                self.__validate_prices(prices[time_period])
        else:
            self.assertTrue(Utils.is_number(prices))

    def __validate_time(self, time_string: str):
        """
        Validate rate entry / exit times

        Args:
            time_string: time in hh:mm format

        Returns:

        """
        time_array = time_string.split(":")

        self.assertEquals(2, len(time_array))

        self.assertTrue(Utils.is_number(time_array[0]))
        self.assertTrue(Utils.is_number(time_array[1]))
