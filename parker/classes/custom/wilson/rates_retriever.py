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

    def update_rates(self, html):
        """ Processes html code and updates RateType and RatePrices models

        Args:
            html (str): Wilson Parking page HTML code that includes rates information

        Returns:
            True or False
        """
        rates = self.get_rates(html)
        Utils.pprint(rates)

    def get_rates(self, html):
        rates_html = self.get_data_by_class_name("section", "rates", html)
        parking_rates = dict()
        for section_name in rates_html.keys():
            if section_name not in self.SECTION_NAMES:
                # TODO: Write into log
                print("Unknown section name: " + section_name)
            else:
                mod = __import__(
                    "parker.classes.custom.wilson.rates_sections." + section_name.lower().replace(" ", "_"),
                    fromlist=['RatesSection'])
                RatesSection = getattr(mod, 'RatesSection')
                rates_section = RatesSection()
                rates_section.set_section_data(rates_html[section_name])
                rates_section.get_details(parking_rates)

        return parking_rates
