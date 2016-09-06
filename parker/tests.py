__author__ = 'mpak'
from contextlib import closing
from decimal import *

from django.test import TestCase
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

from parker.models import Parking, RateType, RatePrice
from parker.classes.core.utils import Utils


class WilssonsRateParserMethodTest(TestCase):
    def test_main_drill(self):
        self.maxDiff = None
        # self._get_prices_information_park_id_1()
        self._get_prices_information_park_id_2()

    def _get_prices_information_park_id_1(self):
        url = "http://wilsonparking.com.au/park/2036_Queen-Victoria-Building-Car-Park_111-York-Street-Sydney"

        carpark = Parking.objects.create(parkingID=1, label="Queen Victoria Building Car Park",
                                         address="111 York Street, Sydney",
                                         lat=-33.871109, long=151.206243, parking_type="Wilson", uri=url)

        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['Mon - Fri',
                                                'Overnight Fee: $12.00 fee applies for cars '
                                                'left in the car park past closing',
                                                'Valet Service : $10.00 surcharge applies',
                                                'Public Holidays: Weekend Rates Apply'],
                                      'prices': {30: '7.00',
                                                 60: '24.00',
                                                 90: '38.00',
                                                 120: '46.00',
                                                 150: '56.00',
                                                 180: '56.00',
                                                 1440: '64.00'},
                                      'rate_type': 'hourly'},
                           'Early Bird': {'days': [1, 2, 3, 4, 5],
                                          'entry_end': '09:30',
                                          'entry_start': '08:00',
                                          'exit_end': '19:30',
                                          'exit_start': '15:00',
                                          'prices': '24.00',
                                          'notes': ["Proceed to Level 7 and validate ticket"],
                                          'rate_type': 'flat'},
                           'Super Early Bird': {'days': [1, 2, 3, 4, 5],
                                                'entry_end': '08:00',
                                                'entry_start': '06:00',
                                                'exit_end': '19:30',
                                                'exit_start': '15:00',
                                                'prices': '19.00',
                                                'notes': ["Proceed to Level 7 and validate ticket"],
                                                'rate_type': 'flat'},
                           'Night': {'rates': {0: {'days': [1, 2, 3, 7],
                                                   'entry_start': '17:00',
                                                   'exit_end': '23:59',
                                                   'prices': '12.00',
                                                   'rate_type': 'flat'},
                                               1: {'days': [4, 5, 6],
                                                   'entry_start': '17:00',
                                                   'exit_end': '23:59',
                                                   'prices': '15.00',
                                                   'rate_type': 'flat'}}},
                           'Weekend': {'days': [6, 7],
                                       'entry_start': '00:00',
                                       'exit_end': '23:59',
                                       'notes': ['Sat - Sun', 'Per exit, per day'],
                                       'prices': {30: '7.00',
                                                  60: '7.00',
                                                  90: '16.00',
                                                  120: '16.00',
                                                  150: '21.00',
                                                  180: '21.00',
                                                  1440: '25.00'},
                                       'rate_type': 'hourly'}}

        rates, html = self._get_rates(url)

        # Check rates returned
        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        # Check casual rates stored in DB
        casual_prices = self._get_stored_prices(carpark, "Casual", "hourly", 0)

        for price in casual_prices[0]:
            self.assertEquals(price.price, Decimal(expected_result['Casual']['prices'][price.duration]))

        # Check early bird rates stored in DB
        early_bird_prices = self._get_stored_prices(carpark, "Early Bird", "flat")
        for single_day_price in early_bird_prices:
            self.assertEquals(single_day_price[0].price, Decimal(expected_result['Early Bird']['prices']))

        # Check super early bird rates stored in DB
        super_early_bird_prices = self._get_stored_prices(carpark, "Super Early Bird", "flat")
        for single_day_price in super_early_bird_prices:
            self.assertEquals(single_day_price[0].price, Decimal(expected_result['Super Early Bird']['prices']))

        # Check super early bird rates stored in DB
        # night_prices = self._get_stored_prices(carpark, "Night", "flat")
        # for single_day_price in night_prices:
        #     self.assertEquals(single_day_price[0].price, Decimal(expected_result['Night']['rates']['prices'][0]))

        # Check weekend rates stored in DB
        weekend_prices = self._get_stored_prices(carpark, "Weekend", "flat")
        for single_day_price in weekend_prices:
            self.assertEquals(single_day_price[0].price, Decimal(expected_result['Weekend']['prices']))

    def _get_prices_information_park_id_2(self):
        url = "https://www.wilsonparking.com.au/park/2135_St-Martins-Tower-Car-Park_190-202-Clarence-Street-Sydney"

        rates, html = self._get_rates(url)
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['Public Holidays: Weekend Rates Apply'],
                                      'prices': {30: '9.00',
                                                 60: '29.00',
                                                 90: '54.00',
                                                 120: '54.00',
                                                 150: '65.00',
                                                 180: '65.00',
                                                 210: '74.00',
                                                 240: '74.00',
                                                 1440: '78.00'},
                                      'rate_type': 'hourly'},
                           'Early Bird': {'days': [1, 2, 3, 4, 5],
                                          'entry_end': '09:30',
                                          'entry_start': '08:00',
                                          'exit_end': '19:00',
                                          'exit_start': '15:30',
                                          'prices': '26.00',
                                          'rate_type': 'flat'},
                           'Night': {'rates': {0: {'days': [1, 2, 3],
                                                   'entry_start': '17:00',
                                                   'exit_end': '23:59',
                                                   'prices': '10.00',
                                                   'rate_type': 'flat'},
                                               1: {'days': [4, 5],
                                                   'entry_start': '17:00',
                                                   'exit_end': '23:59',
                                                   'prices': '12.00',
                                                   'rate_type': 'flat'}
                                               }
                                     },
                           'Super Early Bird': {'days': [1, 2, 3, 4, 5],
                                                'entry_end': '08:00',
                                                'entry_start': '07:00',
                                                'exit_end': '19:00',
                                                'exit_start': '15:30',
                                                'prices': '24.00',
                                                'rate_type': 'flat'},
                           'Weekend': {'days': [[6, 7]],
                                       'notes': ['Flate rate per exit, per day'],
                                       'prices': '15.00'}}

        self.assertDictEqual(expected_result, rates)

    def _get_prices_information_park_id_3(self):
        url = "https://www.wilsonparking.com.au/park/2047_Harbourside-Car-Park_100-Murray-Street-Pyrmont"

        rates, html = self._get_rates(url)
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
                                      'prices': {30: '6.00',
                                                 60: '16.00',
                                                 90: '26.00',
                                                 120: '26.00',
                                                 150: '30.00',
                                                 180: '30.00',
                                                 1440: '36.00'},
                                      'rate_type': 'hourly'},
                           'Early Bird': {'days': [1, 2, 3, 4, 5],
                                          'entry_end': '09:30',
                                          'entry_start': '06:00',
                                          'exit end': '19:00',
                                          'exit start': '15:00',
                                          'notes': ['Have ticket validated by machine on '
                                                    'Level 3 in the morning, proceed to '
                                                    'Level 1 or 2 for parking'],
                                          'prices': '$15.00',
                                          'rate_type': 'flat'},
                           'Night': {'entry_start': '18:00',
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

        self.maxDiff = None
        self.assertDictEqual(expected_result, rates)

    def _get_prices_information_park_id_4(self):
        url = "https://www.wilsonparking.com.au/park/2024_175-Liverpool-St-Car-Park_26-Nithsdale-Street-Sydney"

        rates, html = self._get_rates(url)
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['Overnight Rate $30 Monday - Friday',
                                                'Motorbike Rate $5.00',
                                                'Public Holidays: Weekend Rates Apply',
                                                'Saturday April 2nd - car park will be '
                                                'closed between 7:00am and 7:00pm due to '
                                                'building maintenance'],
                                      'prices': {30: '10.00',
                                                 60: '10.00',
                                                 90: '24.00',
                                                 120: '24.00',
                                                 150: '36.00',
                                                 180: '36.00',
                                                 210: '42.00',
                                                 240: '42.00',
                                                 1440: '48.00'},
                                      'rate_type': 'hourly'},
                           'Early Bird': {'days': [1, 2, 3, 4, 5],
                                          'entry_end': '10:00',
                                          'entry_start': '08:00',
                                          'exit end': '19:00',
                                          'exit start': '15:00',
                                          'notes': ['Proceed to Level B4 for parking and '
                                                    'validation of ticket'],
                                          'prices': '$18.00',
                                          'rate_type': 'flat'},
                           'Night': {'entry_start': '17:00',
                                     'exit end': '23:59',
                                     'rates': {0: {'days': [1, 2, 3, 4, 5],
                                                   'prices': '$9.00',
                                                   'rate_type': 'flat'}}},
                           'Super Early Bird': {'days': [1, 2, 3, 4, 5],
                                                'entry_end': '08:00',
                                                'entry_start': '07:00',
                                                'exit end': '19:00',
                                                'exit start': '15:00',
                                                'notes': ['Proceed to Level B4 for parking '
                                                          'and validation of ticket'],
                                                'prices': '$16.00',
                                                'rate_type': 'flat'},
                           'Weekend': {'days': [6, 7],
                                       'entry_start': '00:00',
                                       'exit_end': '23:50',
                                       'notes': ['Flat rate per exit, per day'],
                                       'prices': '$9.00'}}

        self.maxDiff = None
        self.assertDictEqual(expected_result, rates)

    """ This function validates the rates object generated as well as subsequently validates the rates saved and stored in DB
    """

    def _get_prices_information_park_id_5(self):
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['Public Holidays:  Casual Rates Apply',
                                                'Car Park Closed: Fri-25 Dec & Fri-01 Jan'
                                                ],
                                      'prices': {30: "0.00",
                                                 60: "0.00",
                                                 90: "0.00",
                                                 120: "0.00",
                                                 150: "3.00",
                                                 180: "7.00",
                                                 210: "9.00",
                                                 240: "11.00",
                                                 270: "13.00",
                                                 300: "15.00",
                                                 330: "23.00",
                                                 360: "23.00",
                                                 390: "32.00",
                                                 420: "32.00",
                                                 1440: "42.00"},
                                      'rate_type': 'hourly'},
                           }
        url = "https://www.wilsonparking.com.au/park/2260_East-Village-Car-Park_4-Defries-Avenue-Zetland"
        carpark = Parking.objects.create(parkingID=5, label="East Village Car Park",
                                         address="4 Defries Avenue, Zetland",
                                         lat=-33.905890, long=151.210313, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(url)
        self.maxDiff = None
        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)
        rate = RateType.objects.get(parkingID=carpark, label="Casual", rate_type="hourly", day_of_week=0)
        prices = RatePrice.objects.filter(rateID=rate).order_by('duration')

        for price in prices:
            self.assertEquals(price.price, Decimal(expected_result['Casual']['prices'][price.duration]))

    def _get_prices_information_park_id_6(self):
        """This function validates the rates object generated as well as subsequently validates the rates saved and stored in DB
        """
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['Lost ticket $45.00.',
                                                'Public Holidays: Casual Rates Apply'
                                                ],
                                      'prices': {30: "0.00",
                                                 60: "0.00",
                                                 90: "0.00",
                                                 120: "0.00",
                                                 150: "0.00",
                                                 180: "0.00",
                                                 210: "6.00",
                                                 240: "9.00",
                                                 270: "13.00",
                                                 300: "16.00",
                                                 330: "20.00",
                                                 360: "25.00",
                                                 390: "30.00",
                                                 420: "40.00",
                                                 1440: "45.00"},
                                      'rate_type': 'hourly'},
                           }
        url = "https://www.wilsonparking.com.au/park/2219_Macquarie-Shopping-Centre-Car-Park_Cnr-Herring--Waterloo-Roads-North-Ryde-"
        carpark = Parking.objects.create(parkingID=6, label="Macquarie Shopping Centre Car Park",
                                         address="Cnr Herring & Waterloo Roads, North Ryde",
                                         lat=-33.776880, long=151.118162, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(url)
        self.maxDiff = None
        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)
        rate = RateType.objects.get(parkingID=carpark, label="Casual", rate_type="hourly", day_of_week=0)
        prices = RatePrice.objects.filter(rateID=rate).order_by('duration')

        for price in prices:
            self.assertEquals(price.price, Decimal(expected_result['Casual']['prices'][price.duration]))

    def _get_prices_information_park_id_7(self):
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['Public Holidays:  Weekend Rates Apply',
                                                'Student Rate: $20.00 per exit per day.\nMust validate ticket at UTS or Ultimo TAFE',
                                                ],
                                      'prices': {
                                          30: "6.00",
                                          60: "15.00",
                                          90: "25.00",
                                          120: "25.00",
                                          150: "30.00",
                                          180: "30.00",
                                          210: "34.00",
                                          240: "34.00",
                                          1440: "39.00"},
                                      'rate_type': 'hourly'},
                           'Night': {'notes': ['Special Events: $28.00'],
                                     'rates': {0: {'days': [1, 2, 3, 4, 5, 6, 7],
                                                   'entry_start': '16:00',
                                                   'exit_end': '04:00',
                                                   'prices': '12.00',
                                                   'rate_type': 'flat'
                                                   },
                                               }},
                           'Weekend': {'days': [6, 7],
                                       'notes': ['Per exit, per day'],
                                       'entry_start': '00:00',
                                       'exit_end': '23:59',
                                       'prices': {30: '7.00',
                                                  60: '10.00',
                                                  1440: '20.00'},
                                       'rate_type': 'hourly'}
                           }
        url = "https://www.wilsonparking.com.au/park/2108_169-179-Thomas-Street-Car-Park_169-179-Thomas-Street-Haymarket"
        carpark = Parking.objects.create(parkingID=7, label="169-179 Thomas Street Car Park",
                                         address="169-179 Thomas Street Car Park",
                                         lat=-33.881828, long=151.2005398, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(url)
        self.maxDiff = None
        self.assertDictEqual(expected_result, rates)

        # self._update_rates(carpark, html)
        # rate = RateType.objects.get(parkingID=carpark, label="Casual", rate_type="hourly", day_of_week=0)
        # prices = RatePrice.objects.filter(rateID=rate).order_by('duration')
        #
        # for price in prices:
        #     self.assertEquals(price.price, Decimal(expected_result['Casual']['prices'][price.duration]))

    def _get_rates(self, url):
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

            return rates, browser.page_source

    def _update_rates(selfs, carpark, html):
        mod = __import__("parker.classes.custom.wilson.rates_retriever",
                         fromlist=['RatesRetriever'])

        RatesRetriever = getattr(mod, 'RatesRetriever')
        parser = RatesRetriever()
        parser.update_rates(carpark, html)

    def _get_stored_prices(self, carpark, rate_label, rate_type, day_of_week=-1):
        # rates are QuerySets
        rates = RateType.objects.filter(parkingID=carpark, label=rate_label, rate_type=rate_type)

        if day_of_week > -1:
            rates = rates.filter(day_of_week=day_of_week)

        prices = []
        for rate in rates:
            prices.append(RatePrice.objects.filter(rateID=rate).order_by('duration'))

        return prices
