import re

from parker.classes.core.utils import Utils


class WilsonRates:
    ENTRY_EXIT_TIMES_REGEX = "([0-9]{1,2}[pam]{0,2})(?:\:)?([0-9]{1,2}[pam]{0,2})?"

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
        """Initialize Willsons Parking rates object."""
        self.parking_type = "Wilson"
        self.rates_data = []
        self.processed_rates = dict()
        self.processed_lines = []

    def set_section_data(self, section_data):
        self.rates_data = section_data

    def _unset_processed_lines(self):
        for line_to_remove in self.processed_lines:
            self.rates_data.remove(line_to_remove)
        self.processed_lines = []

    def _extract_times_from_line(self, line):
        times_list = line.split(",")

        entry_times = []
        for entry_list in re.compile(self.ENTRY_EXIT_TIMES_REGEX).findall(times_list[0]):
            entry_times.append(list(filter(None, entry_list)))  # Filtering out empty strings

        exit_times = []
        for exit_list in re.compile(self.ENTRY_EXIT_TIMES_REGEX).findall(times_list[1]):
            exit_times.append(list(filter(None, exit_list)))  # Filtering out empty strings

        return {"entry": entry_times, "exit": exit_times}

    def _extract_hourly_rates(self):
        i = 0
        current_hourly_minutes = 0
        for line in self.rates_data:
            if Utils.string_found('hrs', line) or Utils.string_found(' days', line):
                if not i + 1 == len(self.rates_data):
                    next_line = self.rates_data[i + 1]
                    prices_str = self._format_prices_line(next_line)

                    if Utils.string_found(" - ", line):
                        time_str = self._format_time_line(line)
                        hours_arr = time_str.split(" - ")
                        if hours_arr[1] != "24.0":
                            offset = float(hours_arr[1]) - float(hours_arr[0])
                            current_hourly_minutes += 30
                            self.processed_rates['prices'][current_hourly_minutes] = prices_str

                            if offset > 0.5:
                                number_of_repetitions = offset / 0.5
                                for z in range(1, int(number_of_repetitions)):
                                    current_hourly_minutes += 30
                                    self.processed_rates['prices'][current_hourly_minutes] = prices_str
                        else:
                            self.processed_rates['prices'][self.MINUTES_IN_24_HOURS] = prices_str
                    elif Utils.string_found(" days", line):
                            number_of_days = self._format_time_line(line)
                            current_hourly_minutes = int(float(number_of_days) * self.MINUTES_IN_24_HOURS)
                            self.processed_rates['prices'][current_hourly_minutes] = prices_str
                    elif Utils.string_found("+", line):
                        self.processed_rates['prices'][self.MINUTES_IN_24_HOURS] = prices_str

                    self.processed_lines.append(line)
                    if next_line:
                        self.processed_lines.append(next_line)
            i += 1

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
