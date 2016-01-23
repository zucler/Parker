from parker.classes.parsers.core.parser import CoreParser
from parker.classes.rates.wilson.rates import Rates


class RatesParser(CoreParser):
    """Willsons Parking extension of HTML parser class"""

    def __init__(self):
        """Initialize Willsons Parking HTML parser."""
        CoreParser.__init__(self)
        self.__sectionNames = ["Casual", "Early Bird", "Night", "Weekend"]
        self.__sectionHtmlTag = "<h3>"

    def get_prices_information(self, html):
        """Process html code to build and return a parking rates object

        Args:
                html (str): Willsons Parking page html that includes parking info

        Returns:
                Returns Rates object that contain parking rates information
        """
        raw_rates = {}
        willsons_rates = Rates()
        rates_html = self.get_data_by_class_name("section", "rates", html).strip()
        sections_dict = self.split_rates_by_sections(self.__sectionHtmlTag, rates_html)

        # Creating formatted array of parking prices
        for section_name in sections_dict.keys():
            if section_name not in self.__sectionNames:
                # TODO: Write into log
                print("Unknown section name: " + section_name)
            else:
                raw_rates[section_name] = sections_dict[section_name].splitlines()

        willsons_rates.feed(raw_rates)

        return willsons_rates

    def _get_raw_rates_for_section(self, section_name, section_html):
        """Extracts data HTML for a specified section (e.g. Casual) and returns this data as a list

        Args:
                current_section (str): name of the currently parsed section

        Returns:
                Filters HTML data relevant to the provided section and returns it at a list
        """
        result = ""
        rates_html_iterator = iter(section_html.splitlines())
        for line in rates_html_iterator:
            current_section_header = "<h3>" + current_section + "</h3>"
            if current_section_header in line:
                section_started = True

            if section_started:
                if self._entered_new_section(line, current_section_header):
                    break
                else:
                    result += line + "\n"

        result = result.splitlines()
        return result

    def _entered_new_section(self, line, current_section_header):
        """Detects section headers in a single HTML line. Returns True or False

        Args:
                line (str): HTML line
                current_section_html (str): HTML header for current section

        Returns:
                Returns true if new section HTML is detected in current line, false otherwise
        """
        for another_section in self.__sectionNames:
            another_section_html = "<h3>" + another_section + "</h3>"
            if another_section_html == current_section_header:
                continue
            if another_section_html in line:
                return True

        return False
