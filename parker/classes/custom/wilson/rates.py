import re

from parker.classes.core.utils import Utils


class WilsonRates:
    ENTRY_EXIT_TIMES_REGEX = "([0-9]{1,2}[pam]{0,2})(?:\:)?([0-9]{1,2}[pam]{0,2})?|(midnight)|(exit before car park closes)"

    MINUTES_IN_24_HOURS = 1440

    DAYS_OF_WEEK = [
        ["Mon", "Monday"],
        ["Tue", "Tuesday", "Tues"],
        ["Wed", "Wednesday"],
        ["Thu", "Thursday", "Thurs"],
        ["Fri", "Friday"],
        ["Sat", "Saturday"],
        ["Sun", "Sunday"]
    ]

    def __init__(self):
        """Initialize Wilson Parking rates object."""
        self.parking_type = "Wilson"
        self.rates_data = []
        self.processed_rates = dict()
        self.processed_lines = []
        self.hourly_minutes = 0

    def set_section_data(self, section_data):
        self.rates_data = section_data

    def _unset_processed_lines(self):
        for line_to_remove in self.processed_lines:
            try:
                self.rates_data.remove(line_to_remove)
            except ValueError:
                Utils.pprint("Following line does not exist in the list: ")
                Utils.pprint(line_to_remove)
                exit("Error while processing rates")
        self.processed_lines = []

    def _extract_times_from_line(self, line):
        times_list = self.__split_times_string_into_list(line)

        entry_times = []
        for entry_list in re.compile(self.ENTRY_EXIT_TIMES_REGEX).findall(times_list[0]):
            entry_times.append(list(filter(None, entry_list)))  # Filtering out empty strings

        exit_times = []
        for exit_list in re.compile(self.ENTRY_EXIT_TIMES_REGEX).findall(times_list[1]):
            exit_times.append(list(filter(None, exit_list)))  # Filtering out empty strings

        return {"entry": entry_times, "exit": exit_times}

    def __split_times_string_into_list(self, time_str: str):
        split_characters = [",", "and"]

        for split_char in split_characters:
            times_list = time_str.split(split_char)

            if len(times_list) == 2:
                return times_list

        raise Exception("Can not split times string into list ", time_str)

    def _extract_hourly_rates(self):
        i = 0
        for line in self.rates_data:
            if Utils.string_found('hrs', line) or Utils.string_found(' days', line):
                if not i + 1 == len(self.rates_data):
                    next_line = self.rates_data[i + 1]
                    price = self._format_prices_line(next_line)

                    if Utils.string_found(" - ", line):
                        time_str = self._format_time_line(line)
                        self._store_rates_for_hourly_rage(time_str, price)
                    elif Utils.string_found(" days", line):
                        number_of_days = self._format_time_line(line)
                        self._store_rates_for_daily_range(number_of_days, price)
                    elif Utils.string_found("+", line):
                        self._store_rates_for_daily_range(1, price)

                    self.processed_lines.append(line)
                    if next_line:
                        self.processed_lines.append(next_line)
            i += 1

    def _store_rates_for_hourly_rage(self, time_str, price):
        hours_arr = time_str.split(" - ")
        if hours_arr[1] != "24.0":
            offset = float(hours_arr[1]) - float(hours_arr[0])
            self.hourly_minutes += 30
            self.processed_rates['prices'][self.hourly_minutes] = price

            if offset > 0.5:
                number_of_repetitions = offset / 0.5
                for z in range(1, int(number_of_repetitions)):
                    self.hourly_minutes += 30
                    self.processed_rates['prices'][self.hourly_minutes] = price
        else:
            self.processed_rates['prices'][self.MINUTES_IN_24_HOURS] = price

    def _store_rates_for_daily_range(self, number_of_days, price):
        time_range_in_minutes = int(float(number_of_days) * self.MINUTES_IN_24_HOURS)
        self.processed_rates['prices'][time_range_in_minutes] = price

    def is_a_day(self, string):
        """Detect if string is a day of week

        Args:
                string (str): string to compare
        """
        for day_list in self.DAYS_OF_WEEK:
            for day in day_list:
                if Utils.string_found(day, string):
                    return True
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

    def _detect_days_in_range(self, days_range):
        """Read a string and return a list of all days in it

        Args:
                days_range (str): Mon-Fri

        Returns:
                Returns list of all the days included in range
        """
        if Utils.string_found(" - ", days_range):
            self.__start_day, self.__end_day = days_range.split(" - ")
        elif Utils.string_found(" & ", days_range):
            self.__start_day, self.__end_day = days_range.split(" & ")
        else:
            for day_list in self.DAYS_OF_WEEK:
                for day in day_list:
                    if days_range.lower() == day.lower():
                        return [Utils.day_string_to_digit(day_list[0])]

        self.__range_started = False
        self.__list_of_days = []
        result = False
        max_iterations = 2
        iteration = 1
        while not result and iteration <= max_iterations:
            result = self._loop_through_days()
            iteration += 1

        self.__list_of_days.sort()
        return self.__list_of_days

    def _loop_through_days(self):
        for day_list in self.DAYS_OF_WEEK:
            day_added = False
            for day in day_list:

                if self.__start_day.lower() == day.lower():
                    self.__range_started = True

                if self.__range_started and not day_added:
                    self.__list_of_days.append(Utils.day_string_to_digit(day_list[0]))
                    day_added = True

                if self.__range_started and self.__end_day.lower() == day.lower():
                    return True

    def _format_time_line(self, line):
        """Remove unnecessary bits from hours string

        Args:
                line (str): Hours string
        """
        line = line.replace("hrs", "")
        line = line.replace("days", "")
        return line.strip()

    def _format_prices_line(self, line):
        """Remove unnecessary bits from prices string

        Args:
                line (str): Rate string
        """
        if Utils.string_found("$", line):
            return line[1:].strip()
        elif Utils.string_found("free", line.lower()):
            return "0.00"
        else:
            return line
