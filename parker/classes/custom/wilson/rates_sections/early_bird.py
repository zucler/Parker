from parker.classes.core.utils import Utils
from parker.classes.custom.wilson.rates import WilsonRates


# @TODO: Add Extended Early Bird
class RatesSection(WilsonRates):
    # Need to create a new dictionary with all the possible titles that exist fot the section. It will help us to
    # filter incorrect section titles in _is_title_in_line() function

    SECTIONS_DICTIONARY = {
        "Super Early Bird": ["Super Early Bird", "Super EB", "Super Earlybird"],
        "Early Bird": ["Early Bird", "EB", "Earlybird"]
    }

    SECTIONS_PROCESSING_ORDER = ["Super Early Bird", "Early Bird"]  # EARLY BIRD SHOULD ALWAYS BE PROCESSED LAST

    def __init__(self):
        """ Init Early Bird Rates Section

        Returns:

        """
        WilsonRates.__init__(self)
        self.unprocessed_raw_data = []

    def get_details(self, parking_rates):
        """ Extracts early bird rates information from raw data provided

        Args:
            parking_rates (list): List of all parking rates

        Returns:
            Returns dictionary of Early Bird and Super Early Bird data
        """
        self.unprocessed_raw_data = self.rates_data.copy()

        for section_key in self.SECTIONS_PROCESSING_ORDER:
            self._process_rates(section_key, self.SECTIONS_DICTIONARY[section_key])
            self._unset_processed_lines()

        self._process_days()
        self._unset_processed_lines()

        if self.rates_data:
            for rate_type in self.processed_rates.keys():
                if "prices" in self.processed_rates[rate_type].keys():
                    self.processed_rates[rate_type]['notes'] = self.rates_data

        for rate_type in self.processed_rates.keys():
            if "prices" in self.processed_rates[rate_type].keys():
                parking_rates[rate_type] = self.processed_rates[rate_type]

    def _process_days(self):
        for line in self.unprocessed_raw_data:
            if self.is_a_day(line):  # Check if a line has days information
                line_saved = False
                for section_key in self.SECTIONS_PROCESSING_ORDER:
                    section_titles = self.SECTIONS_DICTIONARY[section_key]
                    if self._is_title_in_line(line, section_titles) and "days" not in self.processed_rates[section_key].keys():
                        line = self._extract_day_string(section_titles, line)
                        self.processed_rates[section_key]['days'] = self._detect_days_in_range(line)
                        line_saved = True

                if not line_saved:
                    for rate_type in self.processed_rates.keys():
                        if "prices" in self.processed_rates[rate_type].keys():
                            self.processed_rates[rate_type]["days"] = self._detect_days_in_range(line)

                if line in self.rates_data:
                    self.processed_lines.append(line)

    def _extract_day_string(self, titles_list, line):
        for title in titles_list:
            if Utils.string_found(title.lower(), line.lower()):
                line = line.lower().replace(title.lower(), "").strip()
                return line

    def _process_rates(self, dict_key, titles_list):
        """ Parses raw rates data provided and builds a structured dictionary of information

        Args:
            titles_list (list): List of either early bird or super early bird titles
            dict_key (str): Dictionary key to be used to store processed data against

        Returns:
            Stores processed data in self.processed_rates dictionary
        """
        self.processed_rates[dict_key] = dict()
        i = 0
        for line in self.rates_data:
            next_line = ""
            if not i + 1 == len(self.rates_data):
                next_line = self.rates_data[i + 1]

            # If current line is a header, and next one is price
            if self._do_save_rates(titles_list, dict_key, line, next_line):
                self.processed_rates[dict_key]["prices"] = next_line
                self.processed_lines.append(line)
                self.processed_lines.append(next_line)
                self.processed_rates[dict_key]["rate_type"] = "flat"
            # Else if current line is Entry & Exit times
            elif self._do_save_times_data(titles_list, dict_key, line):
                times_dict = self._extract_times_from_line(line)
                self.processed_lines.append(line)

                self.processed_rates[dict_key]["entry start"] = Utils.convert_to_24h_format(":".join(times_dict['entry'][0]))
                self.processed_rates[dict_key]["entry end"] = Utils.convert_to_24h_format(":".join(times_dict['entry'][1]))
                self.processed_rates[dict_key]["exit start"] = Utils.convert_to_24h_format(":".join(times_dict['exit'][0]))
                self.processed_rates[dict_key]["exit end"] = Utils.convert_to_24h_format(":".join(times_dict['exit'][1]))

            i += 1

    def _do_save_rates(self, titles_list, dict_key, line, next_line):
        if Utils.string_found("$", next_line):
            if self._is_title_in_line(line, titles_list):
                return True
            elif self._is_single_rate_parking() and dict_key == "Early Bird":
                return True

        return False

    def _do_save_times_data(self, titles_list, dict_key, line):
        if Utils.string_found("entry", line.lower()):
            if self._is_title_in_line(line, titles_list):
                return True
            elif self._is_single_rate_parking():
                return True

        return False

    def _is_single_rate_parking(self):
        count = 0
        for section_name in self.SECTIONS_PROCESSING_ORDER:
            for line in self.unprocessed_raw_data:
                if self._is_title_in_line(line, self.SECTIONS_DICTIONARY[section_name]):
                    count += 1
                    break

        if count == 1 or count == 0:  # Added this and exception for test purposes. Once confirmed that logic is working, both should be removed
            return True

        if count > 1:
            return False

        return False

    def _is_title_in_line(self, line, header_titles):
        """ Checks if HTML line provied has a section title in it

        Args:
            line (str): subject to search line
            header_titles (list): list of title variations

        Returns:

        """
        # THIS FUNCTION ONLY WORKS IF EARLY BIRD IS PROCESSED LAST
        for title in header_titles:
            if Utils.string_found(title.lower(), line.lower()):
                return True
        return False
