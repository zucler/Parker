from parker.classes.core.utils import Utils
from parker.classes.custom.wilson.rates import WilsonRates


class RatesSection(WilsonRates):
    LABEL = "Weekend"

    def __init__(self):
        WilsonRates.__init__(self)

    def get_details(self, parking_rates):
        # Ignore if casual rates apply
        if len(self.rates_data) == 1:
            if Utils.string_found("casual rates apply", self.rates_data[0].lower()):
                return

        self.processed_rates['prices'] = dict()
        # self.processed_rates['days'] = []
        parking_rates[self.LABEL] = dict()

        # Checking first three lines for hourly rate
        is_hourly_rate = False

        for i in range(0, 2):
            if self._is_hourly_rate(self.rates_data[i]):
                is_hourly_rate = True

        if is_hourly_rate:
            self._extract_hourly_rates()
            self.processed_rates['days'] = [6, 7]
            self.processed_rates['rate_type'] = "hourly"
            self.processed_rates['entry_start'] = "00:00"
            self.processed_rates['exit_end'] = "23:59"
        else:
            # Checking for flat rates
            if self.is_a_day(self.rates_data[0]):
                line_index = 0
                self.processed_rates['days'] = []
                for line in self.rates_data:
                    if not line_index + 1 == len(self.rates_data):
                        next_line = self.rates_data[line_index + 1]

                    if self.is_a_day(line):
                        self.processed_rates['days'].append(self._detect_days_in_range(line))
                        self.processed_lines.append(line)

                        if Utils.string_found("$", next_line):
                            self.processed_rates['prices'] = Utils.format_price_string(next_line)
                            self.processed_lines.append(next_line)

                    line_index += 1

        self._unset_processed_lines()

        parking_rates[self.LABEL] = self.processed_rates

        if self.rates_data:
            parking_rates[self.LABEL]["notes"] = self.rates_data
