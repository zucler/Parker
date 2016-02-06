from parker.classes.custom.wilson.types import RateTypes
from parker.classes.core.utils import Utils
import re


class RatesSection():
    SUPER_EARLY_BIRD_KEY = "super early bird"
    SUPER_EARLY_BIRD_HTML_TITLES = ["super early bird", "super eb", "super earlybird"]
    ENTRY_EXIT_TIMES_REGEX = "([0-9]{1,2}[pam]{0,2})(?:\:)?([0-9]{1,2}[pam]{0,2})?"

    def __init__(self):
        self.rates_data = ""
        self.unprocessed_rates_data = ""
        self.processed_rates = dict()
        self.processed_rates[self.SUPER_EARLY_BIRD_KEY] = dict()

    def get_details(self, raw_data):
        self.rates_data = self.unprocessed_rates_data = raw_data
        self._process_super_early_bird_rates()
        #self._process_early_bird_rates()
        #self.extract_days()  # go throw original rates_data list and pick up every line that has days in it and decide which type it should go to
        Utils.pprint(self.processed_rates)
        exit()

    def _process_super_early_bird_rates(self):
        """ Parses raw rates data provided and builds a structured dictionary of information

        Returns:
            Stores processed data in self.processed_rates dictionary
        """
        i = 0
        for line in self.rates_data:
            if not i + 1 == len(self.rates_data):
                next_line = self.rates_data[i + 1]

            # If current line is a header, and next one is price
            if self._is_title_in_line(line, self.SUPER_EARLY_BIRD_HTML_TITLES) and Utils.string_found("$", next_line):
                self.processed_rates[self.SUPER_EARLY_BIRD_KEY]["price"] = next_line
                self.unprocessed_rates_data.pop(self.unprocessed_rates_data.index(line))
                self.unprocessed_rates_data.pop(self.unprocessed_rates_data.index(next_line))
            # Else if current line is Entry & Exit times
            elif self._is_title_in_line(line, self.SUPER_EARLY_BIRD_HTML_TITLES) and Utils.string_found("entry", line.lower()):
                times_list = line.split(",")

                entry_times = []
                for entry_list in re.compile(self.ENTRY_EXIT_TIMES_REGEX).findall(times_list[0]):
                    entry_times.append(list(filter(None, entry_list)))  # Filtering out empty strings

                exit_times = []
                for exit_list in re.compile(self.ENTRY_EXIT_TIMES_REGEX).findall(times_list[1]):
                    exit_times.append(list(filter(None, exit_list)))  # Filtering out empty strings

                self.processed_rates[self.SUPER_EARLY_BIRD_KEY]["entry start"] = Utils.convert_to_24h_format(":".join(entry_times[0]))
                self.processed_rates[self.SUPER_EARLY_BIRD_KEY]["entry end"] = Utils.convert_to_24h_format(":".join(entry_times[1]))
                self.processed_rates[self.SUPER_EARLY_BIRD_KEY]["exit start"] = Utils.convert_to_24h_format(":".join(exit_times[0]))
                self.processed_rates[self.SUPER_EARLY_BIRD_KEY]["exit end"] = Utils.convert_to_24h_format(":".join(exit_times[1]))

                self.unprocessed_rates_data.pop(self.unprocessed_rates_data.index(line))

            i += 1

    def _is_title_in_line(self, line, header_titles):
        for title in header_titles:
            if Utils.string_found(title, line.lower()):
                return True

        return False
