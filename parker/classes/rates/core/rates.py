__author__ = 'Maxim Pak'

from parker.classes.utils import Utils


class CoreRates:
    """Generic parking rates class
    This class is a generic storage of parking rates for any car park.

    Attributes:
            types (array): Key => Value like mapping of each prices section name and its' type (e.g. hourly/flat rates)
            rates (array): Array of rates sections
            daysOfWeek (list): List of all days in the week
    """

    def __init__(self):
        """Initialize a generic rates object."""

        self.types = {}
        self.rates = {}
        self.daysOfWeek = ['Mon', "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def is_a_day(self, string):
        """Detect if string is a day of week

        Args:
                string (str): string to compare
        """
        for day in self.daysOfWeek:
            if Utils.string_found(day, string):
                return True
        return False
