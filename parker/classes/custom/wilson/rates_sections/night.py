from parker.classes.custom.wilson.rates import WilsonRates
from parker.classes.core.utils import Utils
import re


class RatesSection(WilsonRates):
    LABEL = "Night"

    def __init__(self):
        WilsonRates.__init__(self)
        self.processed_rates['rates'] = dict()

    def get_details(self, section_data, parking_rates):
        line_index = 0
        i = 0
        for line in section_data:
            if not line_index + 1 == len(section_data):
                next_line = section_data[line_index + 1]

            if self.is_a_day(line):
                self.processed_rates['rates'][i] = dict()
                self.processed_rates['rates'][i]['days'] = self._detect_days_in_range(line)
                self.processed_rates['rates'][i]['prices'] = next_line
                self.processed_rates['rates'][i]['rate_type'] = "flat"
                self.processed_lines.append(line)
                self.processed_lines.append(next_line)
                i += 1

            if Utils.string_found("entry", line.lower()):
                times_dict = self._extract_times_from_line(line)

                self.processed_rates["entry start"] = Utils.convert_to_24h_format(":".join(times_dict['entry'][0]))

                if times_dict['exit']:
                    self.processed_rates["exit end"] = Utils.convert_to_24h_format(":".join(times_dict['exit'][0]))
                else:
                    self.processed_rates["exit end"] = "23:59"  # @TODO: Fix me

                self.processed_lines.append(line)

            line_index += 1

        for line_to_remove in self.processed_lines:
            section_data.remove(line_to_remove)

        parking_rates[self.LABEL] = self.processed_rates

        if section_data:
            parking_rates[self.LABEL]["notes"] = section_data

