from parker.classes.custom.wilson.rates import WilsonRates
from parker.classes.core.utils import Utils
import re

class RatesSection(WilsonRates):
    def __init__(self):
        WilsonRates.__init__(self)
        self.rates_data = ""
        self.processed_rates = dict()

    def get_details(self, section_data):
        Utils.pprint(section_data)
        exit()
        self.processed_rates['entry_start'] = "00:00"
        self.processed_rates['exit_end'] = "23:59"
        self.processed_rates['days_range'] = ""

        # Taken from rates.py REFACTOR
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
                prices[1440] = prices_str  # 1440 is 24 hours in minutes
        """
        {   'early bird': {   'days': [1, 2, 3, 4, 5],
                      'entry end': '09:30',
                      'entry start': '06:00',
                      'exit end': '19:00',
                      'exit start': '15:00',
                      'price': '$15.00'},
        """

        rate_details['days_range'] = []  # casual rate is applicable everyday

        return rate_details

