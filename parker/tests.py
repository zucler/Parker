__author__ = 'mpak'
import os
from decimal import *

from django.test import TestCase
from django.conf import settings

from parker.models import Parking, RateType, RatePrice
from parker.classes.core.utils import Utils


class WilsonsRateParserTest(TestCase):
    fixtures = ['parker.json']

    def test_main(self):
        carparks = Parking.objects.all()

        for carpark in carparks:
            carpark_rates, html = self._get_rates(carpark)

            for section_name in carpark_rates:
                self._validate_section(section_name, carpark_rates[section_name])

    def _validate_section(self, section_name, section_data):
        if section_name == 'Early Bird':
            self._validate_early_bird(section_data)

        if section_name == 'Super Early Bird':
            self._validate_early_bird(section_data)

        if section_name == 'Night':
            self._validate_night(section_data)

        if section_name == 'Weekend':
            self._validate_weekend(section_data)

        if section_name == 'Casual':
            self._validate_casual(section_data)

    def _validate_early_bird(self, section_data):
        some_stuff = ""

    def _validate_night(self, section_data):
        some_stuff = ""

    def _validate_weekend(self, section_data):
        some_stuff = ""

    def _validate_casual(self, section_data):
        some_stuff = ""


    def no_test_main_drill(self):
        self.maxDiff = None

        print("Testing carparkID = 1")
        self._get_prices_information_park_id_1()

        print("Testing carparkID = 2")
        self._get_prices_information_park_id_2()

        print("Testing carparkID = 3")
        self._get_prices_information_park_id_3()

        print("Testing carparkID = 4")
        self._get_prices_information_park_id_4()

        print("Testing carparkID = 5")
        self._get_prices_information_park_id_5()

        print("Testing carparkID = 6")
        self._get_prices_information_park_id_6()

        print("Testing carparkID = 7")
        self._get_prices_information_park_id_7()

        print("Testing carparkID = 8")
        self._get_prices_information_park_id_8()

        print("Testing carparkID = 9")
        self._get_prices_information_park_id_9()

        # print("Testing carparkID = 10")
        # self._get_prices_information_park_id_10()

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
                                          'notes': ["Proceed to Level 7 and validate ticket in "
                                                    'morning, park on Level 7'],
                                          'rate_type': 'flat'},
                           'Super Early Bird': {'days': [1, 2, 3, 4, 5],
                                                'entry_end': '08:00',
                                                'entry_start': '06:00',
                                                'exit_end': '19:30',
                                                'exit_start': '15:00',
                                                'prices': '19.00',
                                                'notes': ["Proceed to Level 7 and validate ticket in "
                                                          'morning, park on Level 7'],
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

        rates, html = self._get_rates(carpark)

        # Check rates returned
        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

    def _get_prices_information_park_id_2(self):
        url = "https://www.wilsonparking.com.au/park/2135_St-Martins-Tower-Car-Park_190-202-Clarence-Street-Sydney"

        carpark = Parking.objects.create(parkingID=2, label="St Martins Tower Car Park",
                                         address="190-202 Clarence Street, Sydney",
                                         lat=-33.871420, long=151.203594, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(carpark)
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
                           'Weekend': {'days': [6, 7],
                                       'entry_start': '00:00',
                                       'exit_end': '23:59',
                                       'rate_type': 'flat',
                                       'notes': ['Flate rate per exit, per day'],
                                       'prices': '15.00'}}

        # Check rates returned
        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

    def _get_prices_information_park_id_3(self):
        url = "https://www.wilsonparking.com.au/park/2047_Harbourside-Car-Park_100-Murray-Street-Pyrmont"

        carpark = Parking.objects.create(parkingID=3, label="Carpark 3",
                                         address="Whatever",
                                         lat=-33.871109, long=151.206243, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(carpark)
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
                                                 1440: '38.00'},
                                      'rate_type': 'hourly'},
                           'Early Bird': {'days': [1, 2, 3, 4, 5],
                                          'entry_end': '09:30',
                                          'entry_start': '06:00',
                                          'exit_end': '19:00',
                                          'exit_start': '15:00',
                                          'notes': ['Have ticket validated by machine on '
                                                    'Level 3 in the morning, proceed to '
                                                    'Level 1 or 2 for parking'],
                                          'prices': '15.00',
                                          'rate_type': 'flat'},
                           'Night': {'rates': {0: {'days': [1, 2, 3, 4],
                                                   'entry_start': '18:00',
                                                   'exit_end': '04:00',
                                                   'prices': '15.00',
                                                   'rate_type': 'flat'},
                                               1: {'days': [5],
                                                   'entry_start': '18:00',
                                                   'exit_end': '04:00',
                                                   'prices': '25.00',
                                                   'rate_type': 'flat'},
                                               2: {'days': [6],
                                                   'entry_start': '18:00',
                                                   'exit_end': '04:00',
                                                   'prices': '25.00',
                                                   'rate_type': 'flat'},
                                               3: {'days': [7],
                                                   'entry_start': '18:00',
                                                   'exit_end': '04:00',
                                                   'prices': '15.00',
                                                   'rate_type': 'flat'}}}
                           }

        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

    def _get_prices_information_park_id_4(self):
        url = "https://www.wilsonparking.com.au/park/2024_175-Liverpool-St-Car-Park_26-Nithsdale-Street-Sydney"

        carpark = Parking.objects.create(parkingID=4, label="Carpark 4",
                                         address="Whatever",
                                         lat=-33.871109, long=151.206243, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(carpark)
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['Overnight Rate $30 Monday - Friday',
                                                'Motorbike Rate $5.00',
                                                'Public Holidays: Weekend Rates Apply'],
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
                                          'exit_end': '19:00',
                                          'exit_start': '15:00',
                                          'notes': ['Proceed to Level B4 for parking and '
                                                    'validation of ticket'],
                                          'prices': '18.00',
                                          'rate_type': 'flat'},
                           'Night': {'rates': {0: {'days': [1, 2, 3, 4, 5],
                                                   'entry_start': '17:00',
                                                   'exit_end': '23:59',
                                                   'prices': '9.00',
                                                   'rate_type': 'flat'}}},
                           'Super Early Bird': {'days': [1, 2, 3, 4, 5],
                                                'entry_end': '08:00',
                                                'entry_start': '07:00',
                                                'exit_end': '19:00',
                                                'exit_start': '15:00',
                                                'notes': ['Proceed to Level B4 for parking '
                                                          'and validation of ticket'],
                                                'prices': '16.00',
                                                'rate_type': 'flat'},
                           'Weekend': {'days': [6, 7],
                                       'entry_start': '00:00',
                                       'exit_end': '23:59',
                                       'notes': ['Flat rate per exit, per day'],
                                       'prices': '9.00',
                                       'rate_type': 'flat'
                                       }}

        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

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
                                                 150: "5.00",
                                                 180: "8.00",
                                                 210: "12.00",
                                                 240: "16.00",
                                                 1440: "18.00"},
                                      'rate_type': 'hourly'},
                           }
        url = "https://www.wilsonparking.com.au/park/2260_East-Village-Car-Park_4-Defries-Avenue-Zetland"
        carpark = Parking.objects.create(parkingID=5, label="East Village Car Park",
                                         address="4 Defries Avenue, Zetland",
                                         lat=-33.905890, long=151.210313, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(carpark)

        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

    def _get_prices_information_park_id_6(self):
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

        rates, html = self._get_rates(carpark)

        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

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
                                          90: "26.00",
                                          120: "26.00",
                                          150: "31.00",
                                          180: "31.00",
                                          210: "35.00",
                                          240: "35.00",
                                          1440: "40.00"},
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

        rates, html = self._get_rates(carpark)

        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

    def _get_prices_information_park_id_8(self):
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'notes': ['First 15 minutes free in open air car park (P9)',
                                                'Rates are based on a 24 hour period',
                                                'Each additional 24 hour period, or part thereof: $59.50 '
                                                'per day'],
                                      'prices': {
                                          30: "8.00",
                                          60: "17.00",
                                          90: "25.00",
                                          120: "25.00",
                                          150: "33.00",
                                          180: "33.00",
                                          1440: "59.50",
                                          2880: "119.00",
                                          4320: "178.50"},
                                      'rate_type': 'hourly'}
                           }
        url = "https://www.wilsonparking.com.au/park/2099_Sydney-Airport-International-Car-Park_Sydney-International-Airport-Station-Mascot"
        carpark = Parking.objects.create(parkingID=8, label="169-179 Thomas Street Car Park",
                                         address="169-179 Thomas Street Car Park",
                                         lat=-33.881828, long=151.2005398, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(carpark)

        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

    def _get_prices_information_park_id_9(self):
        url = "https://www.wilsonparking.com.au/park/4062_Eagle-Street-Pier-Car-Park_45-Eagle-Street-Brisbane"

        carpark = Parking.objects.create(parkingID=9, label="Carpark 9",
                                         address="Whatever",
                                         lat=-27.468988, long=153.028419, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(carpark)
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'prices': {30: '10.00',
                                                 60: '23.00',
                                                 90: '46.00',
                                                 120: '46.00',
                                                 150: '69.00',
                                                 180: '69.00',
                                                 210: '74.00',
                                                 240: '74.00',
                                                 270: '79.00',
                                                 300: '79.00',
                                                 330: '84.00',
                                                 360: '84.00',
                                                 1440: '89.00'},
                                      'rate_type': 'hourly'},
                           'Night': {'rates': {0: {'days': [1, 2, 3, 4, 5],
                                                   'entry_start': '17:00',
                                                   'exit_end': '06:00',
                                                   'prices': '15.00',
                                                   'rate_type': 'flat'}}},
                           'Weekend': {'days': [6, 7],
                                       'entry_start': '00:00',
                                       'exit_end': '23:59',
                                       'notes': ['RIVERFIRE 24/09/2016',
                                                 '$20.00',
                                                 'Flat rate per exit, per day.'],
                                       'prices': '15.00',
                                       'rate_type': 'flat'
                                       }}

        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

    def _get_prices_information_park_id_10(self):
        url = "https://www.wilsonparking.com.au/park/3296_425-Collins-Street_425-Collins-Street"

        carpark = Parking.objects.create(parkingID=10, label="Carpark 10",
                                         address="Whatever",
                                         lat=-37.817492, long=144.958452, parking_type="Wilson", uri=url)

        rates, html = self._get_rates(carpark)
        expected_result = {'Casual': {'days': '',
                                      'entry_start': '00:00',
                                      'exit_end': '23:59',
                                      'prices': {30: '20.00',
                                                 60: '20.00',
                                                 90: '42.00',
                                                 120: '42.00',
                                                 150: '62.00',
                                                 180: '62.00',
                                                 210: '65.00',
                                                 240: '65.00',
                                                 270: '70.00',
                                                 300: '70.00'
                                                 },
                                      'rate_type': 'hourly'},
                           'Early Bird': {'days': [1, 2, 3, 4, 5],
                                          'entry_end': '10:00',
                                          'entry_start': '06:00',
                                          'exit_end': '19:00',
                                          'exit_start': '10:00',
                                          'prices': '27.00',
                                          'rate_type': 'flat'}
                           }

        self.assertDictEqual(expected_result, rates)

        self._update_rates(carpark, html)

        self._assert_saved_rates(carpark, expected_result)

    def _get_rates(self, carpark: Parking):
        html_file = os.path.join(settings.HTML_CACHE_DIRECTORY, "carparkID_" + str(carpark.parkingID) + ".html")
        rates_file = open(html_file, "rb")
        rates_bytes = rates_file.read()
        rates_html = rates_bytes.decode("utf-8")
        rates_file.close()

        mod = __import__("parker.classes.custom." + carpark.parking_type.lower() + ".rates_retriever",
                         fromlist=['RatesRetriever'])
        RatesRetriever = getattr(mod, 'RatesRetriever')
        # store it as string variable
        parser = RatesRetriever()
        rates = parser.get_rates(rates_html)
        return rates, rates_html

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

    def _assert_saved_rates(self, carpark, expected_result):
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
