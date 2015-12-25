__author__ = 'Maxim Pak'

import collections
import re

from parker.classes.utils import Utils


class Rates:
    """Generic parking rates class
    This class is a generic storage of parking rates for any car park.

    Attributes:
            types (array): Key => Value like mapping of each prices section name and its' type (e.g. hourly/flat rates)
            rates (array): Array of rates sections
            daysOfWeek (list): List of all days in the week
    """

    def __init__(self):
        """Initialize a generic rates object."""

        self.types = {}
        self.rates = {}
        self.daysOfWeek = ['Mon', "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def is_a_day(self, string):
        """Detect if string is a day of week

        Args:
                string (str): string to compare
        """
        for day in self.daysOfWeek:
            if Utils.string_found(day, string):
                return True
        return False


class WillsonsRates(Rates):
    def __init__(self):
        """Initialize Willsons Parking rates object."""
        Rates.__init__(self)

    def feed(self, raw_rates):
        """Feed data into object and process it

        Args:
                raw_rates (array): Array of unformatted rates
        """
        for (section_name, rates) in raw_rates.items():
            self.types[section_name] = self._get_rate_type_info(section_name, rates)
            self.rates[section_name] = self._extract_prices_from_raw_list(section_name, rates)

    def _get_rate_type_info(self, section_name, rates):
        """Get information for a rate type (start/end times & rate type)

        Args:
            section_name (str): Name of the rate section (e.g. Early Bird, Night)
            rates: (list): List of HTML entries for the section given

        Returns:
            Returns dictionary of information for a rate
        """
        rate_type = {}

        if section_name == "Early Bird":
            for string in rates:
                if Utils.string_found("Entry between", string):
                    rate_times = re.compile("[0-9:]*am").findall(string)
                    rate_type['start'] = Utils.convert_to_24h_format(rate_times[0])
                    rate_type['end'] = Utils.convert_to_24h_format(rate_times[1])
                    notes_array = string.split(",")
                    rate_type['notes'] = notes_array[1].strip().capitalize()
  
        if section_name == "Night":
            for string in rates:
                if Utils.string_found("Entry after", string):
                    rate_times = re.compile("[0-9:]*pm").findall(string)
                    rate_type['start'] = Utils.convert_to_24h_format(rate_times[0])
                    rate_type['end'] = "23:59"

        if section_name == "Casual":
            rate_type['start'] = "00:00"
            rate_type['end'] = "23:59"

        if section_name == "Weekend":
            rate_type['start'] = "00:00"
            rate_type['end'] = "23:59"

        rate_type['type'] = self._detect_rates_type(rates)

        return rate_type

    def _detect_rates_type(self, rates):
        """Detect type of the rates section

        Args:
                rates (list): Detects whether the section has flat or hourly rates

        Returns:
                "Flat" or "Hourly"
        """
        for string in rates:
            if Utils.string_found(" - ", string):
                if self._is_flat_rate(string):
                    return "Flat"
                elif self._is_hourly_rate(string):
                    return "Hourly"

    def _is_flat_rate(self, string):
        """Detect if rate provided is a flat price

        Args:
                string (str): String with rates

        Returns:
                True if rate is flat. False otherwise
        """
        string_list = string.split(" - ")
        for sub_string in string_list:
            if self.is_a_day(sub_string):
                return True
            else:
                return False

    def _is_hourly_rate(self, string):
        """Detect if rate provided is hourly based

        Args:
                string (str): String with rates

        Returns:
                True if rate is hourly based. False otherwise
        """
        if Utils.string_found("hrs", string):
            return True
        else:
            return False

    def _extract_prices_from_raw_list(self, section_name, rates):
        """Extract parking prices from raw HTML list

        Args:
                section_name (str): Name of the section
                rates (list): List of rates for the section

        Returns:
                Returns formatted prices for every half-hour (for hourly rates) or each day (if flat rate)
        """
        prices = collections.OrderedDict()
        current_hourly_minutes = 0

        for i in range(0, len(rates)):
            line = rates[i]

            # Skips last element in the list
            if not i + 1 == len(rates):
                next_line = rates[i + 1]
            else:
                break

            # Process hourly section
            if self.types[section_name] == "Hourly":

                if Utils.string_found('hrs', line):
                    hours_str = self._format_hours_line(line)
                    prices_str = self._format_prices_line(next_line)

                    hours_arr = hours_str.split(" - ")
                    if len(hours_arr) == 2:
                        offset = float(hours_arr[1]) - float(hours_arr[0])
                        current_hourly_minutes += 30
                        prices[current_hourly_minutes] = prices_str

                        if offset == 1.0:
                            current_hourly_minutes += 30
                            prices[current_hourly_minutes] = prices_str
                    else:
                        prices[str(current_hourly_minutes) + "+"] = prices_str

            # Process flat price section
            if self.types[section_name] == "Flat":
                if self.is_a_day(line):
                    days_range = self._detect_days_in_range(line)
                    flat_price = self._format_prices_line(next_line)
                    for day in days_range:
                        prices[day] = flat_price

        return prices

    def _detect_days_in_range(self, days_range):
        """Read a string and return a list of all days in it

        Args:
                days_range (str): Mon-Fri

        Returns:
                Returns list of all the days included in range
        """
        try:
            self.__start_date, self.__end_date = days_range.split(" - ")
        except Exception:
            return [days_range]

        self.__range_started = False
        self.__list_of_days = []
        result = False
        max_iterations = 2
        iteration = 1
        while not result or iteration == max_iterations:
            result = self._loop_through_days()
            ++iteration
        return self.__list_of_days

    def _loop_through_days(self):
        for day in self.daysOfWeek:
            if self.__start_date == day:
                self.__range_started = True

            if self.__range_started:
                self.__list_of_days += [day]

            if self.__range_started and self.__end_date == day:
                return True

    def _format_hours_line(self, line):
        """Remove unnecessary bits from hours string

        Args:
                line (str): Hours string
        """
        return line[:-3].strip()

    def _format_prices_line(self, line):
        """Remove unnecessary bits from prices string

        Args:
                line (str): Rate string
        """
        return line[1:].strip()
