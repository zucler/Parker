from parker.classes.custom.wilson.rates import WilsonRates
from parker.classes.custom.wilson.rates_sections import casual
from parker.classes.core.utils import Utils

class RatesSection(WilsonRates):
    LABEL = "Weekend"

    def __init__(self):
        WilsonRates.__init__(self)
        self.rates_data = ""
        self.processed_rates = dict()

    def get_details(self, section_data, parking_rates):
        self.rates_data = section_data
        self.processed_rates['prices'] = dict()
        self.processed_rates['days'] = []

        # Ignore if casual rates apply
        if len(self.rates_data) == 1:
            if Utils.string_found("casual rates apply", section_data[0].lower()):
                return

        # Checking for hourly rate
        if Utils.string_found("hrs", self.rates_data[0]):
            self._extract_hourly_rates(self.rates_data)
            parking_rates['days'] = [6, 7]

        # Checking for flat rates
        if self.is_a_day(self.rates_data[0]):
            line_index = 0
            for line in self.rates_data:
                if not line_index + 1 == len(self.rates_data):
                    next_line = section_data[line_index + 1]

                if self.is_a_day(line):
                    self.processed_rates['days'].append(self._detect_days_in_range(line))
                    self.processed_lines.append(line)

                    if Utils.string_found("$", next_line):
                        self.processed_rates['prices'] = next_line
                        self.processed_lines.append(next_line)

                line_index += 1

        for line_to_remove in self.processed_lines:
            self.rates_data.remove(line_to_remove)

        parking_rates[self.LABEL] = self.processed_rates

        if section_data:
            parking_rates["notes"] = self.rates_data
