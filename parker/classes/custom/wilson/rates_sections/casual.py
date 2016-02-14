from parker.classes.custom.wilson.rates import WilsonRates


class RatesSection(WilsonRates):
    LABEL = "Casual"

    def __init__(self):
        WilsonRates.__init__(self)

    def get_details(self, parking_rates):
        self.processed_rates['entry_start'] = "00:00"
        self.processed_rates['exit_end'] = "23:59"
        self.processed_rates['days'] = ""
        self.processed_rates['rate_type'] = "hourly"
        self.processed_rates['prices'] = dict()

        self._extract_hourly_rates()
        self._unset_processed_lines()

        parking_rates[self.LABEL] = self.processed_rates

        if self.rates_data:
            parking_rates[self.LABEL]["notes"] = self.rates_data
