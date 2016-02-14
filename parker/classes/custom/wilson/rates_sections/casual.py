from parker.classes.custom.wilson.rates import WilsonRates
from parker.classes.core.utils import Utils


class RatesSection(WilsonRates):
    LABEL = "Casual"

    def __init__(self):
        WilsonRates.__init__(self)

    def get_details(self, section_data, parking_rates):
        self.processed_rates['entry_start'] = "00:00"
        self.processed_rates['exit_end'] = "23:59"
        self.processed_rates['days'] = ""
        self.processed_rates['prices'] = dict()

        self._extract_hourly_rates(section_data)

        for line_to_remove in self.processed_lines:
            section_data.remove(line_to_remove)

        parking_rates[self.LABEL] = self.processed_rates

        if section_data:
            parking_rates[self.LABEL]["notes"] = section_data

