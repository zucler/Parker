__author__ = 'Maxim Pak'
import re
from datetime import datetime


class Utils:
    """Class to group all static utility methods together."""

    @staticmethod
    def string_found(search_for, search_subject):
        """Find string in larger string with a simple regex.

        Args:
                search_for (str): a string to search for
                search_subject (str): a string to search within

        Returns:
                Returns True if string is found. False otherwise
        """
        if re.search(r"\b" + re.escape(search_for) + r"\b", search_subject):
            return True
        return False

    @staticmethod
    def string_has_match_in_list(array, search_subject):
        """Find a match for a string in a list.

        Args:
                array (list): list of strings to match
                search_subject(str): a string to search within

        Returns:
                Returns True if match is found. False otherwise.
        """
        for item in array:
            if re.search(r"\b" + re.escape(item) + r"\b", search_subject):
                return True

        return False

    @staticmethod
    def convert_to_24h_format(time):
        """Convert HH:MM, HH or H 12 hours time into 24 HH:MM format

        Args:
            time (string): Time in HH:MM, HH or H 12 hours format

        Returns:
            Returns string representing time in HH:MM 24 hours format
        """
        hours_minutes_12_format = "%I:%M%p"
        hours_only_12_format = "%I%p"
        hours_minutes_24_format = "%H:%M"

        try:
            time = datetime.strptime(time, hours_minutes_12_format).strftime(hours_minutes_24_format)
        except ValueError:
            time = datetime.strptime(time, hours_only_12_format).strftime(hours_minutes_24_format)

        return time
