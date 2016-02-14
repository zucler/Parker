from parker.classes.custom.wilson.rates import WilsonRates
from parker.classes.custom.wilson.rates_sections import casual
from parker.classes.core.utils import Utils

class RatesSection(WilsonRates):
    LABEL = "Weekend"

    def __init__(self):
        WilsonRates.__init__(self)

    def get_details(self, parking_rates):
        self.processed_rates['prices'] = dict()
        self.processed_rates['days'] = []
        parking_rates[self.LABEL] = dict()

        # Ignore if casual rates apply
        if len(self.rates_data) == 1:
            if Utils.string_found("casual rates apply", self.rates_data[0].lower()):
                return

        # Checking for hourly rate
        if Utils.string_found("hrs", self.rates_data[0]):
            self._extract_hourly_rates()
            self.processed_rates['days'] = [6, 7]

        # Checking for flat rates
        if self.is_a_day(self.rates_data[0]):
            line_index = 0
            for line in self.rates_data:
                if not line_index + 1 == len(self.rates_data):
                    next_line = self.rates_data[line_index + 1]

                if self.is_a_day(line):
                    self.processed_rates['days'].append(self._detect_days_in_range(line))
                    self.processed_lines.append(line)

                    if Utils.string_found("$", next_line):
                        self.processed_rates['prices'] = next_line
                        self.processed_lines.append(next_line)

                line_index += 1

        self._unset_processed_lines()

        parking_rates[self.LABEL] = self.processed_rates

        if self.rates_data:
            parking_rates[self.LABEL]["notes"] = self.rates_data
