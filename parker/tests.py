__author__ = 'mpak'

from contextlib import closing

from django.test import TestCase
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait


class WilssonsRateParserMethodTest(TestCase):
    # def test_get_prices_information_park_id_1(self):
    #     url = "http://wilsonparking.com.au/park/2036_Queen-Victoria-Building-Car-Park_111-York-Street-Sydney"
    #
    #     rates = self.get_rates(url)
    #     expected_result = {'Casual': {'days': '',
    #                                   'entry_start': '00:00',
    #                                   'exit_end': '23:59',
    #                                   'notes': ['Overnight Fee: $12.00 fee applies for cars '
    #                                             'left in the car park past closing',
    #                                             'Valet Service : $15.00 surcharge applies',
    #                                             'Public Holidays: Weekend Rates Apply'],
    #                                   'prices': {30: '9.00',
    #                                              60: '21.00',
    #                                              90: '36.00',
    #                                              120: '46.00',
    #                                              150: '56.00',
    #                                              180: '56.00',
    #                                              1440: '64.00'},
    #                                   'rate_type': 'hourly'},
    #                        'Early Bird': {'days': [1, 2, 3, 4, 5],
    #                                       'entry end': '09:30',
    #                                       'entry start': '08:00',
    #                                       'exit end': '19:30',
    #                                       'exit start': '15:00',
    #                                       'prices': '$24.00',
    #                                       'notes': ["Proceed to Level 7 and validate ticket"],
    #                                       'rate_type': 'flat'},
    #                        'Super Early Bird': {'days': [1, 2, 3, 4, 5],
    #                                             'entry end': '08:00',
    #                                             'entry start': '06:00',
    #                                             'exit end': '19:30',
    #                                             'exit start': '15:00',
    #                                             'prices': '$19.00',
    #                                             'notes': ["Proceed to Level 7 and validate ticket"],
    #                                             'rate_type': 'flat'},
    #                        'Night': {'entry start': '17:00',
    #                                  'exit end': '23:59',
    #                                  'rates': {0: {'days': [1, 2, 3, 7],
    #                                                'prices': '$12.00',
    #                                                'rate_type': 'flat'},
    #                                            1: {'days': [4, 5, 6],
    #                                                'prices': '$15.00',
    #                                                'rate_type': 'flat'}}},
    #                        'Weekend': {'days': [6, 7],
    #                                    'notes': ['Per exit, per day'],
    #                                    'prices': {30: '7.00',
    #                                               60: '7.00',
    #                                               90: '16.00',
    #                                               120: '16.00',
    #                                               150: '21.00',
    #                                               180: '21.00',
    #                                               1440: '25.00'},
    #                                    'rate_type': 'hourly'}}
    #
    #     self.maxDiff = None
    #     self.assertDictEqual(expected_result, rates)
    #
    # def test_get_prices_information_park_id_2(self):
    #     url = "https://www.wilsonparking.com.au/park/2135_St-Martins-Tower-Car-Park_190-202-Clarence-Street-Sydney"
    #
    #     rates = self.get_rates(url)
    #     expected_result = {'Casual': {'days': '',
    #                                   'entry_start': '00:00',
    #                                   'exit_end': '23:59',
    #                                   'notes': ['Motorbike Rate $10.00',
    #                                             'Public Holidays: Weekend Rates Apply'],
    #                                   'prices': {30: '9.00',
    #                                              60: '29.00',
    #                                              90: '54.00',
    #                                              120: '54.00',
    #                                              150: '65.00',
    #                                              180: '65.00',
    #                                              210: '74.00',
    #                                              240: '74.00',
    #                                              1440: '78.00'},
    #                                   'rate_type': 'hourly'},
    #                        'Early Bird': {'days': [1, 2, 3, 4, 5],
    #                                       'entry end': '09:30',
    #                                       'entry start': '08:00',
    #                                       'exit end': '19:00',
    #                                       'exit start': '15:30',
    #                                       'prices': '$24.00',
    #                                       'rate_type': 'flat'},
    #                        'Night': {'entry start': '17:00',
    #                                  'exit end': '23:59',
    #                                  'rates': {0: {'days': [1, 2, 3, 4, 5],
    #                                                'prices': '$10.00',
    #                                                'rate_type': 'flat'}}},
    #                        'Super Early Bird': {'days': [1, 2, 3, 4, 5],
    #                                             'entry end': '08:00',
    #                                             'entry start': '07:00',
    #                                             'exit end': '19:00',
    #                                             'exit start': '15:30',
    #                                             'prices': '$22.00',
    #                                             'rate_type': 'flat'},
    #                        'Weekend': {'days': [[6, 7]],
    #                                    'notes': ['Flate rate per exit, per day'],
    #                                    'prices': '$15.00'}}
    #
    #     self.maxDiff = None
    #     self.assertDictEqual(expected_result, rates)
    #
    # def test_get_prices_information_park_id_3(self):
    #     url = "https://www.wilsonparking.com.au/park/2047_Harbourside-Car-Park_100-Murray-Street-Pyrmont"
    #
    #     rates = self.get_rates(url)
    #     expected_result = {'Casual': {'days': '',
    #                                   'entry_start': '00:00',
    #                                   'exit_end': '23:59',
    #                                   'notes': ['Motorcycle',
    #                                             '$14.00',
    #                                             'Rates are calculated from 6:00am daily',
    #                                             'Public Holidays:  Casual Rates Apply',
    #                                             'Motorcycle parkers to park in yellow '
    #                                             'designated areas on Level 4 and contact '
    #                                             'Attendant in Office prior to departure'],
    #                                   'prices': {30: '6.00',
    #                                              60: '16.00',
    #                                              90: '26.00',
    #                                              120: '26.00',
    #                                              150: '30.00',
    #                                              180: '30.00',
    #                                              1440: '36.00'},
    #                                   'rate_type': 'hourly'},
    #                        'Early Bird': {'days': [1, 2, 3, 4, 5],
    #                                       'entry end': '09:30',
    #                                       'entry start': '06:00',
    #                                       'exit end': '19:00',
    #                                       'exit start': '15:00',
    #                                       'notes': ['Have ticket validated by machine on '
    #                                                 'Level 3 in the morning, proceed to '
    #                                                 'Level 1 or 2 for parking'],
    #                                       'prices': '$15.00',
    #                                       'rate_type': 'flat'},
    #                        'Night': {'entry start': '18:00',
    #                                  'exit end': '04:00',
    #                                  'rates': {0: {'days': [1, 2, 3, 4],
    #                                                'prices': '$15.00',
    #                                                'rate_type': 'flat'},
    #                                            1: {'days': 5,
    #                                                'prices': '$25.00',
    #                                                'rate_type': 'flat'},
    #                                            2: {'days': 6,
    #                                                'prices': '$25.00',
    #                                                'rate_type': 'flat'},
    #                                            3: {'days': 7,
    #                                                'prices': '$15.00',
    #                                                'rate_type': 'flat'}}},
    #                        'Weekend': {}}
    #
    #     self.maxDiff = None
    #     self.assertDictEqual(expected_result, rates)
    #
    # def test_get_prices_information_park_id_4(self):
    #     url = "https://www.wilsonparking.com.au/park/2024_175-Liverpool-St-Car-Park_26-Nithsdale-Street-Sydney"
    #
    #     rates = self.get_rates(url)
    #     expected_result = {'Casual': {'days': '',
    #                                   'entry_start': '00:00',
    #                                   'exit_end': '23:59',
    #                                   'notes': ['Overnight Rate $30 Monday - Friday',
    #                                             'Motorbike Rate $5.00',
    #                                             'Public Holidays: Weekend Rates Apply',
    #                                             'Saturday April 2nd - car park will be '
    #                                             'closed between 7:00am and 7:00pm due to '
    #                                             'building maintenance'],
    #                                   'prices': {30: '10.00',
    #                                              60: '10.00',
    #                                              90: '24.00',
    #                                              120: '24.00',
    #                                              150: '36.00',
    #                                              180: '36.00',
    #                                              210: '42.00',
    #                                              240: '42.00',
    #                                              1440: '48.00'},
    #                                   'rate_type': 'hourly'},
    #                        'Early Bird': {'days': [1, 2, 3, 4, 5],
    #                                       'entry end': '10:00',
    #                                       'entry start': '08:00',
    #                                       'exit end': '19:00',
    #                                       'exit start': '15:00',
    #                                       'notes': ['Proceed to Level B4 for parking and '
    #                                                 'validation of ticket'],
    #                                       'prices': '$18.00',
    #                                       'rate_type': 'flat'},
    #                        'Night': {'entry start': '17:00',
    #                                  'exit end': '23:59',
    #                                  'rates': {0: {'days': [1, 2, 3, 4, 5],
    #                                                'prices': '$9.00',
    #                                                'rate_type': 'flat'}}},
    #                        'Super Early Bird': {'days': [1, 2, 3, 4, 5],
    #                                             'entry end': '08:00',
    #                                             'entry start': '07:00',
    #                                             'exit end': '19:00',
    #                                             'exit start': '15:00',
    #                                             'notes': ['Proceed to Level B4 for parking '
    #                                                       'and validation of ticket'],
    #                                             'prices': '$16.00',
    #                                             'rate_type': 'flat'},
    #                        'Weekend': {'days': [6, 7],
    #                                    'notes': ['Flat rate per exit, per day'],
    #                                    'prices': '$9.00'}}
    #
    #     self.maxDiff = None
    #     self.assertDictEqual(expected_result, rates)

    def test_get_prices_information_park_id_5(self):
        url = "https://www.wilsonparking.com.au/park/2260_East-Village-Car-Park_4-Defries-Avenue-Zetland"

        rates = self.get_rates(url)
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['Public Holidays:  Casual Rates Apply',
                                                'Car Park Closed: Fri-25 Dec',
                                                'Fri-01 Jan'
                                                ],
                                      'prices': {30: '0.00',
                                                 60: '0.00',
                                                 90: '0.00',
                                                 120: '0.00',
                                                 150: '3.00',
                                                 180: '7.00',
                                                 210: '9.00',
                                                 240: '11.00',
                                                 270: '13.00',
                                                 300: '15.00',
                                                 330: '23.00',
                                                 360: '23.00',
                                                 390: '32.00',
                                                 420: '32.00',
                                                 1440: '42.00'},
                                      'rate_type': 'hourly'},
                           }

        self.maxDiff = None
        self.assertDictEqual(expected_result, rates)

    def get_rates(self, url):
        mod = __import__("parker.classes.custom.wilson.rates_retriever",
                         fromlist=['RatesRetriever'])

        RatesRetriever = getattr(mod, 'RatesRetriever')

        # use firefox to get page with javascript generated content
        with closing(Firefox()) as browser:
            browser.get(url)
            # wait for the page to load
            WebDriverWait(browser, timeout=10).until(
                lambda x: x.find_element_by_class_name('rates'))
            # store it as string variable
            parser = RatesRetriever()
            rates = parser.get_rates(browser.page_source)

            return rates
