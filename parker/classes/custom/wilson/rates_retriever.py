#from parker.classes.custom.wilson.rate_types import RateTypes

from parker.classes.core.parser import CoreParser
from parker.classes.core.utils import Utils
from parker.classes.custom.wilson.rates import WilsonRates
from parker.models import Parking, RateType, RatePrice


class RatesRetriever(CoreParser):
    """Willsons Parking extension of HTML parser class"""

    SECTION_SPLIT_TAG = "h3"  # Tag that usually represent a start of new section (e.g. Casual, Early Bird)
    SECTION_NAMES = ["Casual", "Early Bird", "Night", "Weekend"]

    def __init__(self):
        """Initialize Willsons Parking HTML parser."""
        CoreParser.__init__(self, self.SECTION_SPLIT_TAG)

    def update_rates(self, carpark, html):
        """ Processes html code and updates RateType and RatePrices models

        Args:
            carpark (Parking): Parking object
            html (str): Wilson Parking page HTML code that includes rates information

        Returns:
            True or False
        """
        rates = self.get_rates(html)
        #Utils.pprint(rates)
        self.store_rates(carpark, rates)

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

    def store_rates(self, carpark, rates):
        """ Stores processed rates object into DB

        Args:
            carpark (Parking): Parking object
            rates (Dictionary): processed dictionary of car parking rates

        Returns:
            N/A

        """
        for rate_section in rates.keys():
            rate = rates[rate_section]
            if rate['rate_type'].lower() == "hourly":
                if rate_section.lower() == "casual":
                    self._store_casual_rate(carpark, rate_section, rate, day)
                else:
                    print("Unknown hourly rate: " + rate_section)
                    return

    def _store_casual_rate (self, carpark, rate):
        """ Stores rate data for casual rate type

        Args:
            carpark (Parking): Parking object
            rate (dict): Dictionary storing rates data

        Returns:

        """
        carpark_rate, created = RateType.objects.get_or_create(parkingID=carpark, label="Casual",
                                                               rate_type=rate['rate_type'],
                                                               day_of_week=0)

        save_carpark_rate = False
        if carpark_rate.start_time != rate['entry_start']:
            carpark_rate.start_time = rate['entry_start']
            save_carpark_rate = True

        if carpark_rate.end_time != rate['exit_end']:
            carpark_rate.end_time = rate['exit_end']
            save_carpark_rate = True

        if save_carpark_rate:
            carpark_rate.save()

        for parking_duration in rate['prices'].keys():
            price = rate['prices'][parking_duration]
            carpark_rate_price, created = RatePrice.objects.get_or_create(rateID=carpark_rate,
                                                                          duration=parking_duration)

            if carpark_rate_price.price != price:
                carpark_rate_price.price = price
                carpark_rate_price.save()
