__author__ = 'Maxim Pak'
import re


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
