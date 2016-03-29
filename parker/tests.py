__author__ = 'mpak'

from contextlib import closing

from django.test import TestCase
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait


class WilssonsRateParserMethodTest(TestCase):
    def test_get_prices_information_park_id_3(self):
        """
        get_prices_information() should return object of type WillsonsParkingRates
        """
        mod = __import__("parker.classes.custom.wilson.rates_retriever",
                         fromlist=['RatesRetriever'])
        RatesRetriever = getattr(mod, 'RatesRetriever')

        url = "https://www.wilsonparking.com.au/park/2047_Harbourside-Car-Park_100-Murray-Street-Pyrmont"

        # use firefox to get page with javascript generated content
        with closing(Firefox()) as browser:
            browser.get(url)
            # wait for the page to load
            WebDriverWait(browser, timeout=10).until(
                lambda x: x.find_element_by_class_name('rates'))
            # store it as string variable
            parser = RatesRetriever()
            rates = parser.get_rates(browser.page_source)

            expected_result = {'Casual': {'days': '',
                                          'entry_start': '00:00',
                                          'exit_end': '23:59',
                                          'notes': ['Motorcycle',
                                                    '$14.00',
                                                    'Rates are calculated from 6:00am daily',
                                                    'Public Holidays:  Casual Rates Apply',
                                                    'Motorcycle parkers to park in yellow '
                                                    'designated areas on Level 4 and contact '
                                                    'Attendant in Office prior to departure'],
                                          'prices': {30: '5.00',
                                                     60: '15.00',
                                                     90: '25.00',
                                                     120: '25.00',
                                                     150: '29.00',
                                                     180: '29.00',
                                                     1440: '35.00'},
                                          'rate_type': 'hourly'},
                               'Early Bird': {'days': [1, 2, 3, 4, 5],
                                              'entry_start': '06:00',
                                              'entry_end': '09:30',
                                              'exit_start': '15:00',
                                              'exit_end': '17:00',
                                              'notes': ['Have ticket validated by machine on '
                                                        'Level 3 in the morning, proceed to '
                                                        'Level 1 or 2 for parking'],
                                              'prices': '$15.00',
                                              'rate_type': 'flat'},
                               'Night': {'entry start': '18:00',
                                         'exit end': '04:00',
                                         'rates': {0: {'days': [1, 2, 3, 4],
                                                       'prices': '$15.00',
                                                       'rate_type': 'flat'},
                                                   1: {'days': 5,
                                                       'prices': '$25.00',
                                                       'rate_type': 'flat'},
                                                   2: {'days': 6,
                                                       'prices': '$25.00',
                                                       'rate_type': 'flat'},
                                                   3: {'days': 7,
                                                       'prices': '$15.00',
                                                       'rate_type': 'flat'}}},
                               'Weekend': {}}

            self.assertDictEqual(expected_result, rates)
