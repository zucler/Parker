from parker.classes.custom.wilson.rates import WilsonRates
from parker.classes.core.utils import Utils


class RatesSection(WilsonRates):
    def __init__(self):
        WilsonRates.__init__(self)
        self.rates_data = ""
        self.processed_rates = dict()

    def get_details(self, section_data):
        self.processed_rates['entry_start'] = "00:00"
        self.processed_rates['exit_end'] = "23:59"
        self.processed_rates['days'] = ""
        self.processed_rates['prices'] = dict()
        self.processed_rates['label'] = "Casual"

        i = 0
        current_hourly_minutes = 0
        for line in section_data:
            if Utils.string_found('hrs', line):
                if not i + 1 == len(section_data):
                    next_line = section_data[i + 1]

                hours_str = self._format_hours_line(line)
                prices_str = self._format_prices_line(next_line)

                hours_arr = hours_str.split(" - ")
                if len(hours_arr) == 2:
                    offset = float(hours_arr[1]) - float(hours_arr[0])
                    current_hourly_minutes += 30
                    self.processed_rates['prices'][current_hourly_minutes] = prices_str

                    if offset == 1.0:
                        current_hourly_minutes += 30
                        self.processed_rates['prices'][current_hourly_minutes] = prices_str
                else:
                    self.processed_rates['prices'][1440] = prices_str  # 1440 is 24 hours in minutes

            i += 1

        return self.processed_rates

