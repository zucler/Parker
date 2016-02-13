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
        Utils.pprint(section_data)

        # Ignore if casual rates apply
        if len(section_data) == 1:
            if Utils.string_found("casual rates apply", section_data[0].lower()):
                return




