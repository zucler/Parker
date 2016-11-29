import os
import re
import pprint
from datetime import datetime
from parker.models.common import Parking
from django.conf import settings


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

        if search_subject.find(search_for) != -1:  # Test for single special characters
            return True

        if search_for in search_subject:
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
    def string_has_partial_match_in_list(array, search_subject):
        """
        Iterate through each element in the list and return True if it string found in list

        Args:
            array:
            search_subject:

        Returns:

        """
        for item in array:
            if Utils.string_found(item, search_subject):
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

        # TODO: REFACTOR ASAP
        if time == "midnight" or time == "exit before car park closes":
            time = datetime.strptime("00:00", hours_minutes_24_format).strftime(hours_minutes_24_format)
            return time

        try:
            time = datetime.strptime(time, hours_minutes_12_format).strftime(hours_minutes_24_format)
        except ValueError:
            time = datetime.strptime(time, hours_only_12_format).strftime(hours_minutes_24_format)

        return time

    @staticmethod
    def pprint(to_print):
        """ Pretty prints variable
        Args:
            to_print (mixed): Variable to print

        Returns:
            void
        """
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(to_print)

    @staticmethod
    def day_string_to_digit(day_string):
        days = {
            1: ("mon", "monday"),
            2: ("tue", "tuesday"),
            3: ("wed", "wednesday"),
            4: ("thu", "thursday"),
            5: ("fri", "friday"),
            6: ("sat", "saturday"),
            7: ("sun", "sunday")
        }

        for day_number in days.keys():
            if day_string.lower() in days[day_number]:
                return day_number

        return False

    @staticmethod
    def generate_end_html_tag(start_tag: str):
        """ Generates end tag based on the start tag

        Args:
            start_tag: Opening HTML tag

        Returns:
            Returns closing HTML tag
        """
        end_tag = start_tag[:1] + "/" + start_tag[1:]

        return end_tag

    @staticmethod
    def format_price_string(price_string):
        """ Return formatted price string

        Args:
            price_string (string): Price string

        Returns:
            Returns formatted price string
        """

        price_string = price_string.replace("$", "")
        return price_string

    @staticmethod
    def is_number(s):
        """ Check if string is a number or not

        Args:
            s (str):

        Returns:

        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_rates(carpark: Parking):
        """
        Retrieve car park rates from cached HTML

        Args:
            carpark: car park that rates to be returned for

        Returns:
            rates (dict): dictionary of car park rates
        """
        html_file = os.path.join(settings.HTML_CACHE_DIRECTORY, "carparkID_" + str(carpark.parkingID) + ".html")
        rates_file = open(html_file, "rb")
        rates_bytes = rates_file.read()
        rates_html = rates_bytes.decode("utf-8")
        rates_file.close()

        mod = __import__("parker.classes.custom." + carpark.parking_type.lower() + ".rates_retriever",
                         fromlist=['RatesRetriever'])
        rates_retriever_cls = getattr(mod, 'RatesRetriever')
        # store it as string variable
        parser = rates_retriever_cls()
        rates = parser.get_rates(rates_html)
        return rates
