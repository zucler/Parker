#from parker.classes.custom.wilson.rate_types import RateTypes

from parker.classes.core.parser import CoreParser
from parker.classes.core.utils import Utils
from parker.classes.custom.wilson.rates import WilsonRates


class RatesRetriever(CoreParser):
    """Willsons Parking extension of HTML parser class"""

    SECTION_SPLIT_TAG = "h3"  # Tag that usually represent a start of new section (e.g. Casual, Early Bird)
    SECTION_NAMES = ["Casual", "Early Bird", "Night", "Weekend"]

    def __init__(self):
        """Initialize Willsons Parking HTML parser."""
        CoreParser.__init__(self, self.SECTION_SPLIT_TAG)


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

        Utils.pprint(rates_html)
        exit()
        sections_dict = self.split_rates_by_sections(RateTypes.sectionHtmlTag, rates_html)

        # Creating formatted array of parking prices
        for section_name in sections_dict.keys():
            if section_name not in RateTypes.sectionNames:
                # TODO: Write into log
                print("Unknown section name: " + section_name)
            else:
                raw_rates[section_name] = sections_dict[section_name].splitlines()

        willsons_rates.feed(raw_rates)

        return willsons_rates

    def update_rates(self, html):
        """ Processes html code and updates RateType and RatePrices models

        Args:
            html (str): Wilson Parking page HTML code that includes rates information

        Returns:
            True or False
        """
        rates_html = self.get_data_by_class_name("section", "rates", html)
        parking_rates = dict()
        for section_name in rates_html.keys():
            if section_name not in self.SECTION_NAMES:
                # TODO: Write into log
                print("Unknown section name: " + section_name)
            else:
                #print("Section is " + section_name)
                mod = __import__("parker.classes.custom.wilson.rates_sections." + section_name.lower().replace(" ", "_"), fromlist=['RatesSection'])
                RatesSection = getattr(mod, 'RatesSection')
                rates_section = RatesSection()
                rates_section.get_details(rates_html[section_name], parking_rates)

                # if section_name == "Weekend":
                #     rates_section.get_details(rates_html[section_name], parking_rates)

        Utils.pprint(parking_rates)
