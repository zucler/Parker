from parker.classes.core.utils import Utils
from parker.classes.custom.wilson.rates import WilsonRates


class RatesSection(WilsonRates):
    LABEL = "Night"

    def __init__(self):
        WilsonRates.__init__(self)
        self.processed_rates['rates'] = dict()

    def get_details(self, parking_rates):
        entry_start = ""
        exit_end = ""
        line_index = 0
        i = 0

        # Ignore if casual rates apply
        if len(self.rates_data) == 1:
            if Utils.string_found("casual rates apply", self.rates_data[0].lower()):
                return

        for line in self.rates_data:
            if not line_index + 1 == len(self.rates_data):
                next_line = self.rates_data[line_index + 1]

            if self.is_a_day(line):
                self.processed_rates['rates'][i] = dict()
                self.processed_rates['rates'][i]['days'] = self._detect_days_in_range(line)
                self.processed_rates['rates'][i]['prices'] = Utils.format_price_string(next_line)
                self.processed_rates['rates'][i]['rate_type'] = "flat"
                self.processed_lines.append(line)
                self.processed_lines.append(next_line)
                i += 1

            if Utils.string_found("entry", line.lower()):
                times_dict = self._extract_times_from_line(line)

                entry_start = Utils.convert_to_24h_format(":".join(times_dict['entry'][0]))

                if times_dict['exit']:
                    exit_end = Utils.convert_to_24h_format(":".join(times_dict['exit'][0]))
                else:
                    exit_end = "23:59"  # TODO: Fix me

                self.processed_lines.append(line)

            line_index += 1

        for index, rate in self.processed_rates['rates'].items():
            self.processed_rates['rates'][index]['entry_start'] = entry_start
            self.processed_rates['rates'][index]['exit_end'] = exit_end

        self._unset_processed_lines()

        parking_rates[self.LABEL] = self.processed_rates

        if self.rates_data:
            parking_rates[self.LABEL]["notes"] = self._process_notes_data()

    def _process_notes_data(self):
        i = 0
        notes = []
        to_remove = []
        for line in self.rates_data:
            i = i
            if not line:
                self.rates_data.remove(line)

            if Utils.string_found("special events", line.lower()):
                special_events_list = [self.rates_data[i], self.rates_data[i + 1]]
                to_remove.append(self.rates_data[i])
                to_remove.append(self.rates_data[i+1])
                note = ": ".join(special_events_list)
                notes.append(note)

            i += 1

        for line in to_remove:
            self.rates_data.remove(line)

        if self.rates_data:
            notes.append(self.rates_data)

        return notes
