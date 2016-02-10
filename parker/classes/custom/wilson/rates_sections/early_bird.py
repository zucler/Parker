from parker.classes.custom.wilson.rates import WilsonRates
from parker.classes.core.utils import Utils
import re

# @TODO: Add Extended Early Bird
class RatesSection(WilsonRates):
    SUPER_EARLY_BIRD_KEY = "super early bird"
    SUPER_EARLY_BIRD_HTML_TITLES = ["super early bird", "super eb", "super earlybird"]
    EARLY_BIRD_KEY = "early bird"
    EARLY_BIRD_HTML_TITLES = ["early bird", "eb", "earlybird"]

    def __init__(self):
        """ Init Early Bird Rates Section

        Returns:

        """
        WilsonRates.__init__(self)
        self.rates_data = ""
        self.processed_rates = dict()
        self.processed_rates[self.SUPER_EARLY_BIRD_KEY] = dict()
        self.processed_rates[self.EARLY_BIRD_KEY] = dict()

    def get_details(self, raw_data):
        """ Extracts early bird rates information from raw data provided

        Args:
            raw_data (list): List of Early bird lines

        Returns:
            Returns dictionary of Early Bird and Super Early Bird data
        """
        self.rates_data = raw_data
        self.processed_rates['label'] = "Early Bird"

        self._process_rates(self.SUPER_EARLY_BIRD_HTML_TITLES, self.SUPER_EARLY_BIRD_KEY)
        self._process_rates(self.EARLY_BIRD_HTML_TITLES, self.EARLY_BIRD_KEY)
        self._process_days()

        return self.processed_rates

    def _process_days(self):
        for line in self.rates_data:
            if self.is_a_day(line):  # Check if a line has days information
                # Check if days are specific to a certain rate
                if self._is_title_in_line(line, self.SUPER_EARLY_BIRD_HTML_TITLES):
                    line = self._extract_day_string(self.SUPER_EARLY_BIRD_HTML_TITLES, line)
                    self.processed_rates[self.SUPER_EARLY_BIRD_KEY]['days'] = self._detect_days_in_range(line)
                elif self._is_title_in_line(line, self.EARLY_BIRD_HTML_TITLES):
                    line = self._extract_day_string(self.EARLY_BIRD_HTML_TITLES, line)
                    self.processed_rates[self.EARLY_BIRD_KEY]['days'] = self._detect_days_in_range(line)
                else:
                    for rate_type in self.processed_rates.keys():
                        if "price" in self.processed_rates[rate_type].keys():
                            self.processed_rates[rate_type]["days"] = self._detect_days_in_range(line)

    def _extract_day_string(self, titles_list, line):
        for title in titles_list:
            if Utils.string_found(title, line.lower()):
                line = line.lower().replace(title, "").strip()
                return line

    def _process_rates(self, titles_list, dict_key):
        """ Parses raw rates data provided and builds a structured dictionary of information

        Args:
            titles_list (list): List of either early bird or super early bird titles
            dict_key (str): Dictionary key to be used to store processed data against

        Returns:
            Stores processed data in self.processed_rates dictionary
        """
        i = 0
        for line in self.rates_data:
            next_line = ""
            if not i + 1 == len(self.rates_data):
                next_line = self.rates_data[i + 1]

            # If current line is a header, and next one is price
            if self._do_save_rates(titles_list, dict_key, line, next_line):
                self.processed_rates[dict_key]["price"] = next_line
                self.processed_rates[dict_key]["rate_type"] = "flat"
            # Else if current line is Entry & Exit times
            elif self._do_save_times_data(titles_list, dict_key, line):
                times_dict = self._extract_times_from_line(line)

                self.processed_rates[dict_key]["entry start"] = Utils.convert_to_24h_format(":".join(times_dict['entry'][0]))
                self.processed_rates[dict_key]["entry end"] = Utils.convert_to_24h_format(":".join(times_dict['entry'][1]))
                self.processed_rates[dict_key]["exit start"] = Utils.convert_to_24h_format(":".join(times_dict['exit'][0]))
                self.processed_rates[dict_key]["exit end"] = Utils.convert_to_24h_format(":".join(times_dict['exit'][1]))

            i += 1

    def _do_save_rates(self, titles_list, dict_key, line, next_line):
        if Utils.string_found("$", next_line):
            if self._is_title_in_line(line, titles_list):
                return True
            elif self._is_single_rate_parking(dict_key):
                return True

        return False

    def _do_save_times_data(self, titles_list, dict_key, line):
        if Utils.string_found("entry", line.lower()):
            if self._is_title_in_line(line, titles_list):
                return True
            elif self._is_single_rate_parking(dict_key):
                return True

        return False

    def _is_single_rate_parking(self, dict_key):
        # Super EB does not exist, everything default to just EB
        if dict_key == self.EARLY_BIRD_KEY and "price" not in self.processed_rates[self.SUPER_EARLY_BIRD_KEY]:
            return True

        return False

    def _is_title_in_line(self, line, header_titles):
        """ Checks if HTML line provied has a section title in it

        Args:
            line (str): subject to search line
            header_titles (list): list of title variations

        Returns:

        """
        for title in header_titles:
            if Utils.string_found(title, line.lower()):
                return True

        return False
